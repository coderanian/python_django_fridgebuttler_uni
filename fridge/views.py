import re
from urllib import parse

import django.contrib.auth
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render
from datetime import date, timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse

# Touples for expirtion check - 1 = perishable category, 0 = non-perishable
CATEGORIES_EXPIRATION = (
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 0),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),
    (9, 0),
    (10, 0),
    (11, 1),
    (12, 0),
    (13, 0),
    (14, 0)
)


# Create your views here.
def login_redirect(request):
    return redirect('login')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('fridge_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            print(user)
            if user is not None:
                django.contrib.auth.login(request, user)
                return redirect('fridge_list')
            else:
                messages.error(request, 'Combination between username and password does not exist')
    form = LoginForm()
    return render(request, "account/login.html", {'page_title': 'Login into your account', 'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('fridge_list')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)

            safety_question = SecurityQuestions()
            safety_question.user = user
            safety_question.answer = form.cleaned_data.get('security_question')
            safety_question.save()

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    return render(request, "account/account_form.html", {'page_title': 'Registration',
                                                         'submit_button_text': 'Register',
                                                         'form': form})


@login_required(login_url='login')
def logout_user(request):
    django.contrib.auth.logout(request)
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    sq_answer = SecurityQuestions.objects.get(user=user)
                    sq_form_value = form.cleaned_data.get('security_question')
                    sq = ("" or sq_form_value)
                    if sq_answer is not None:
                        if sq_answer.answer.lower() == sq.lower():
                            password1 = form.cleaned_data.get('password1')
                            password2 = form.cleaned_data.get('password2')
                            if password1 == password2:
                                user.set_password(password1)
                                user.save()
                                messages.success(request, 'Successfully updated the password')
                                return redirect('login')
                messages.error(request, 'Combination of user and security question answer does not exists')
                form = ForgotPasswordForm()
            except User.DoesNotExist or SecurityQuestions.DoesNotExist:
                form = ForgotPasswordForm()
                messages.error(request, 'Combination of user and security question answer does not exists')
    else:
        form = ForgotPasswordForm()

    return render(request, "account/account_form.html", {'page_title': 'Forgot password',
                                                         'submit_button_text': 'Reset password',
                                                         'form': form})


@login_required(login_url='login')
def get_fridge_lists(request):
    try:
        fridge_lists = FridgeList.objects.filter(user=request.user)
    except FridgeList.DoesNotExist:
        return redirect('fridge_create')
    return render(request, 'fridge_list/fridge_list.html',
                  {'page_title': 'Overview of fridge lists', 'fridgeLists': fridge_lists})


@login_required(login_url='login')
def edit_fridge_list(request, **kwargs):
    if 'pk' in kwargs:
        try:
            fridge_list = FridgeList.objects.get(pk=kwargs['pk'], user=request.user)
            page_title = f'Edit fridge "{fridge_list.title}"'
        except FridgeList.DoesNotExist:
            return redirect('fridge_list')
    else:
        fridge_list = FridgeList()
        page_title = 'Create new fridge'

    if request.method == 'POST':
        fridge_list.user = request.user
        form = FridgeListForm(request.POST, instance=fridge_list)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fridge list saved!')
            return redirect('fridge_list')
    else:
        form = FridgeListForm(instance=fridge_list)
    return render(request, "fridge_list/edit_fridge.html", {'page_title': page_title, 'form': form})


@login_required(login_url='login')
def delete_fridge(request, **kwargs):
    try:
        fridge = FridgeList.objects.get(pk=kwargs['pk'], user=request.user)
        fridge.delete()
    except FridgeList.DoesNotExist:
        messages.error(request, 'Fridge could not be deleted, please try again later')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def get_expired_fridge_entries(request, **kwargs):
    try:
        fridge = FridgeList.objects.get(id=kwargs['fridgePk'], user=request.user)
        items = FridgeEntry.objects.filter(fridgeList=fridge.id, expired=True, user=request.user)
    except FridgeList.DoesNotExist or FridgeEntry.DoesNotExist:
        return redirect('fridge_list')
    if bool(items) is False:
        return redirect('fridge_items', fridgePk=fridge.id)
    else:
        return render(request, 'fridge_item/fridge_expired.html',
                      {'page_title': f'Expired items in {fridge.title}', 'fridgeEntries': items, 'fridgeId': fridge.id})


@login_required(login_url='login')
def get_fridge_entries(request, **kwargs):
    try:
        fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    except FridgeList.DoesNotExist:
        return redirect('fridge_list')
    try:
        if 'sort_criteria' in kwargs:
            items = FridgeEntry.objects.filter(fridgeList=fridge.id, user=request.user) \
                .order_by(kwargs['sort_criteria'])
        else:
            items = FridgeEntry.objects.filter(fridgeList=fridge.id, user=request.user)
    # Redirect to item edit view if fridge list is empty
    except FridgeEntry.DoesNotExist:
        return redirect('item_create', fridgePk=fridge.id)

    today = date.today()
    for item in items:
        if CATEGORIES_EXPIRATION[item.category - 1][1] == 1:
            # Mark as expired for dynamic CSS if expiration date passed current date
            if item.expirationDate is not None and today > item.expirationDate:
                item.expired = True
                item.save()
            # Allow date change in case of error, otherwise item is always marked as expired
            else:
                item.expired = False
                item.save()

            # If item category is perishable and is opened autoamticaly set expiration date to today + 3 days
            if item.expired == False and item.openedDate:
                date_new = item.openedDate + timedelta(days=3)
                # New expiration date can't be bigger than item's expiration date
                if date_new < item.expirationDate:
                    item.expirationDate = date_new
                    item.save()

            # Mark as soon to expire for dynamic CSS if expiration date in 3 days
            if item.expirationDate is not None and today > (
                    item.expirationDate - timedelta(days=3)):
                item.expiringSoon = True
                item.save()
            # Allow date change in case of error, otherwise item is always marked as expiringSoon
            else:
                item.expiringSoon = False
                item.save()

    return render(request, 'fridge_item/fridge.html',
                  {'page_title': f'Currently stored in {fridge.title}', 'fridgeEntries': items, 'fridgeId': fridge.id})


@login_required(login_url='login')
def edit_fridge_entry(request, **kwargs):
    if 'fridgePk' not in kwargs:
        return redirect('fridge_list')
    else:
        try:
            fridge = FridgeList.objects.get(id=kwargs['fridgePk'], user=request.user)
        except FridgeList.DoesNotExist:
            return redirect('fridge_list')
    # Check if create new item or edit existing one based on kwargs
    if 'itemPk' not in kwargs:
        fridge_entry = FridgeEntry()
        page_title = f'Fridge "{fridge.title}" is empty, create your first entry!'
    else:
        try:
            fridge_entry = FridgeEntry.objects.get(pk=kwargs['itemPk'], user=request.user)
            page_title = f'Edit "{fridge_entry.title}"'
        except FridgeEntry.DoesNotExist:
            return redirect('fridge_items', fridge.id)

    if request.method == 'POST':
        fridge_entry.user = request.user
        entry_form = FridgeEntryForm(request.POST, instance=fridge_entry)
        if entry_form.is_valid():
            # Do not update DB until fridge.id fk is updated with kwargs variable
            new_item = entry_form.save(commit=False)
            new_item.fridgeList = fridge
            new_item.save()
            messages.success(request, 'Fridge entry saved!')
            return redirect('fridge_items', fridgePk=fridge.id)
    else:
        form = FridgeEntryForm(instance=fridge_entry)
    return render(request, "fridge_item/edit_fridge_item.html",
                  {'page_title': page_title, 'form': form, 'fridgePk': fridge.id})


@login_required(login_url='login')
def delete_item(request, **kwargs):
    try:
        item = FridgeEntry.objects.get(id=kwargs['itemPk'], user=request.user)
        item.delete()
    except FridgeEntry.DoesNotExist:
        messages.error(request, 'Fridge item could not be deleted, please try again later')
    return redirect('fridge_items', fridgePk=kwargs['fridgePk'])


@login_required(login_url='login')
def get_shopping_entries(request, **kwargs):
    try:
        fridge = FridgeList.objects.get(id=kwargs['fridgePk'], user=request.user)
        items = BuyListEntry.objects.filter(fridgeList=fridge.id, user=request.user)
    except FridgeList.DoesNotExist or BuyListEntry.DoesNotExist:
        return redirect('shop_item_create', fridgePk=kwargs['fridgePk'])
    return render(request, 'buylist/shopping_list.html',
                  {'page_title': f'Currently needed for {fridge.title}', 'shoppingEntries': items,
                   'fridgeId': fridge.id,
                   'url_name': resolve(request.path).url_name})


@login_required(login_url='login')
def get_shopping_entries_consolidated(request):
    try:
        items = BuyListEntry.objects.filter(user=request.user)
    except FridgeList.DoesNotExist or BuyListEntry.DoesNotExist:
        messages.error(request, 'Nothing on your shopping list, add items via created fridges!')
    return render(request, 'buylist/shopping_list.html',
                  {'page_title': f'Currently needed', 'shoppingEntries': items,
                   'url_name': resolve(request.path).url_name})


@login_required(login_url='login')
def edit_shop_entry(request, **kwargs):
    form = BuyListEntryForm()
    if 'fridgePk' in kwargs:
        try:
            fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
        except FridgeList.DoesNotExist:
            return redirect('fridge_list')
    else:
        return redirect('fridge_list')
    # Check if create new item or edit existing one based on kwargs
    if 'itemPk' in kwargs:
        try:
            shop_entry = BuyListEntry.objects.get(id=kwargs['itemPk'])
            form = BuyListEntryForm(instance=shop_entry)
            page_title = f'Edit "{shop_entry.title}"'
        except BuyListEntry.DoesNotExist:
            return redirect('fridge_list')
    else:
        shop_entry = BuyListEntry()
        page_title = f'Shopping list for "{fridge.title}" is empty, create your first entry!'
    if request.method == 'POST':
        shop_entry.user = request.user
        form = BuyListEntryForm(request.POST, instance=shop_entry)
        if form.is_valid():
            # Do not update DB until fridge.id fk is updated with kwargs variable
            new_item = form.save(commit=False)
            new_item.fridgeList = fridge
            new_item.save()
            return redirect('shop_items', fridgePk=fridge.id)
        else:
            form = BuyListEntryForm(instance=shop_entry)
    return render(request, "buylist/edit_shop_item.html",
                  {'page_title': page_title, 'form': form, 'fridgePk': fridge.id})


@login_required(login_url='login')
def delete_shopping_item(request, **kwargs):
    try:
        item = BuyListEntry.objects.get(id=kwargs['itemPk'], user=request.user)
        item.delete()
    except FridgeList.DoesNotExist or BuyListEntry.DoesNotExist:
        messages.error(request, 'Shopping item could not be deleted, please try again later')
    url_check = re.compile(r"(/fridge/shopping_list/)$")
    # If function called from URL of consolidated shopping list redirect to it instead of shopping list for fridge
    if 'url_name' in kwargs:
        url_name = kwargs['url_name']
    else:
        url_name = request.META.get('HTTP_REFERER')
    # Get original URL function was called from via regex check
    if bool(url_check.search(url_name)) is True:
        return redirect('shop_items_consolidated')
    return redirect('shop_items', fridgePk=kwargs['fridgePk'])


@login_required(login_url='login')
def add_entry_to_fridge(request, **kwargs):
    if 'itemPk' not in kwargs:
        return redirect('fridge_list')
    try:
        item = BuyListEntry.objects.get(id=kwargs['itemPk'], user=request.user)
    except BuyListEntry.DoesNotExist:
        return redirect('shop_items', fridgePk=kwargs['itemPk'])
    url_name = request.META.get('HTTP_REFERER')
    # Prefill model fridgeEntry item with data from buyListEntry
    new_item = FridgeEntry(
        title=item.title,
        category=item.category,
        quantity=item.quantity,
        quantityType=item.quantityType,
        fridgeList=item.fridgeList,
        user=request.user)
    new_item.save()
    messages.success(request, 'Added to fridge and marked as bought!')
    return delete_shopping_item(request, url_name=url_name, **kwargs)


@login_required(login_url='login')
def add_entry_to_shopping_list(request, **kwargs):
    if 'itemPk' not in kwargs:
        return redirect('fridge_list')
    try:
        item = FridgeEntry.objects.get(id=kwargs['itemPk'], user=request.user)
    except BuyListEntry.DoesNotExist:
        return redirect('fridge_items', fridgePk=kwargs['itemPk'])
    # Prefill model buyListEntry item with data from fridgeEntry
    new_item = BuyListEntry(
        title=item.title,
        category=item.category,
        quantity=item.quantity,
        quantityType=item.quantityType,
        fridgeList=item.fridgeList,
        user=request.user)
    new_item.save()
    messages.success(request, 'Added to shopping list!')
    return redirect('fridge_items', fridgePk=item.fridgeList.id)
