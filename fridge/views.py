import django.contrib.auth
from django.shortcuts import render
from datetime import date, timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import *
from django.contrib.auth.decorators import login_required

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

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('fridge_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            print(user)
            if user is not None:
                django.contrib.auth.login(request, user)
                return redirect('fridge_list')
            else:
                messages.error(request, 'Combination between username and password does not exist')
    form = LoginForm()
    return render(request, "account/account.html", {'page_title': 'Login into your account', 'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('fridge_list')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    return render(request, "account/register.html", {'page_title': 'Registration', 'form': form})

def logoutUser(request):
    django.contrib.auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def get_fridge_lists(request):
    fridgeLists = FridgeList.objects.all()
    # Redirect to new list creation if no lists added
    if len(fridgeLists) == 0:
        return redirect('fridge_create')
    return render(request, 'fridge_list/fridge_list.html',
                  {'page_title': 'Overview of fridge lists', 'fridgeLists': fridgeLists})


@login_required(login_url='login')
def edit_fridge_list(request, **kwargs):
    if 'pk' in kwargs:
        pk = kwargs['pk']
    else:
        pk = None
    if pk:
        fridgeList = FridgeList.objects.get(pk=pk)
    else:
        fridgeList = FridgeList()
    if request.method == 'POST':
        form = FridgeListForm(request.POST, instance=fridgeList)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fridge list saved!')
            return redirect('fridge_list')
    else:
        form = FridgeListForm(instance=fridgeList)
    return render(request, "fridge_list/edit_fridge.html", {'page_title': 'Edit fridge list', 'form': form})

@login_required(login_url='login')
def delete_fridge(request, **kwargs):
    fridge = FridgeList.objects.get(pk=kwargs['pk'])
    fridge.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def get_expired_fridge_entries(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    items = FridgeEntry.objects.filter(fridgeList=fridge.id, expired=True)
    if len(items) == 0:
        return redirect('fridge_items', fridgePk=fridge.id)
    return render(request, 'fridge_item/fridge_expired.html',
                  {'page_title': f'Expired items in {fridge.title}', 'fridgeEntries': items, 'fridgeId': fridge.id})

@login_required(login_url='login')
def get_fridge_entries(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    if 'sort_criteria' in kwargs:
        items = FridgeEntry.objects.filter(fridgeList=fridge.id).order_by(kwargs['sort_criteria'])
    else:
        items = FridgeEntry.objects.filter(fridgeList=fridge.id)
    if len(items) == 0:
        return redirect('item_create', fridgePk=fridge.id)
    today = date.today()
    for item in items:
        if CATEGORIES_EXPIRATION[item.category - 1][1] == 1:
            if item.openedDate:
                item.expirationDate = item.openedDate + timedelta(days=3)
                item.save()
            elif item.expirationDate is not None and today > item.expirationDate:
                item.expired = True
                item.save()
            elif item.expirationDate is not None and today > (item.expirationDate - timedelta(days=3)):
                item.expiringSoon = True
                item.save()
    return render(request, 'fridge_item/fridge.html',
                  {'page_title': f'Currently stored in {fridge.title}', 'fridgeEntries': items, 'fridgeId': fridge.id})

@login_required(login_url='login')
def edit_fridge_entry(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    if 'itemPk' in kwargs:
        fridgeEntry = FridgeEntry.objects.get(pk=kwargs['itemPk'])
    else:
        fridgeEntry = FridgeEntry()
    if request.method == 'POST':
        form = FridgeEntryForm(request.POST, instance=fridgeEntry)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.fridgeList = fridge
            new_item.save()
            messages.success(request, 'Fridge entry saved!')
            return redirect('fridge_items', fridgePk=fridge.id)
    else:
        form = FridgeEntryForm(instance=fridgeEntry)
    return render(request, "fridge_item/edit_fridge_item.html",
                  {'page_title': 'Edit fridge item', 'form': form, 'fridgePk': fridge.id})

@login_required(login_url='login')
def delete_item(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    item = FridgeEntry.objects.get(id=kwargs['itemPk'])
    item.delete()
    return redirect('fridge_items', fridgePk=fridge.id)

@login_required(login_url='login')
def get_shopping_entries(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    items = BuyListEntry.objects.filter(fridgeList=fridge.id)
    if len(items) == 0:
        return redirect('shop_item_create', fridgePk=fridge.id)
    return render(request, 'buylist/shopping_list.html',
                  {'page_title': f'Currently needed for {fridge.title}', 'shoppingEntries': items,
                   'fridgeId': fridge.id})

@login_required(login_url='login')
def edit_shop_entry(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    if 'itemPk' in kwargs:
        shopEntry = BuyListEntry.objects.get(id=kwargs['itemPk'])
    else:
        shopEntry = BuyListEntry()
    if request.method == 'POST':
        form = BuyListEntryForm(request.POST, instance=shopEntry)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.fridgeList = fridge
            new_item.save()
            messages.success(request, 'Shopping list entry saved!')
            return redirect('shop_items', fridgePk=fridge.id)
    else:
        form = BuyListEntryForm(instance=shopEntry)
    return render(request, "buylist/edit_shop_item.html",
                  {'page_title': 'Edit fridge item', 'form': form, 'fridgePk': fridge.id})


@login_required(login_url='login')
def delete_shopping_item(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    item = BuyListEntry.objects.get(id=kwargs['itemPk'])
    item.delete()
    return redirect('shop_items', fridgePk=fridge.id)


@login_required(login_url='login')
def add_entry_to_fridge(request, **kwargs):
    item = BuyListEntry.objects.get(id=kwargs['itemPk'])
    new_item = FridgeEntry(
        title=item.title,
        category=item.category,
        quantity=item.quantity,
        quantityType=item.quantityType,
        fridgeList=item.fridgeList)
    new_item.save()
    messages.success(request, 'Added to shopping list!')
    return delete_shopping_item(request, **kwargs)


@login_required(login_url='login')
def add_entry_to_shopping_list(request, **kwargs):
    item = FridgeEntry.objects.get(id=kwargs['itemPk'])
    new_item = BuyListEntry(
        title=item.title,
        category=item.category,
        quantity=item.quantity,
        quantityType=item.quantityType,
        fridgeList=item.fridgeList)
    new_item.save()
    messages.success(request, 'Added to shopping list!')
    return redirect('fridge_items', fridgePk=item.fridgeList.id)