from django.shortcuts import render
from fridge.models import *
from fridge.forms import *
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView


# Create your views here.
def login_redirect(request):
    return redirect('login')


def login(request):
    form = LoginForm()
    return render(request, "account.html", {'page_title': 'Login into your account', 'form': form})


def register(request):
    account = Account()
    form = LoginForm(request.POST, instance=account)
    if form.is_valid():
        form.save()
        messages.success(request, 'Registration completed!')
        return HttpResponseRedirect(reverse_lazy('login'))
    return render(request, "registrationDummy", {'page_title': 'Registration', 'form': form})


def get_fridge_lists(request):
    fridgeLists = FridgeList.objects.all()
    # Redirect to new list creation if no lists added
    if len(fridgeLists) == 0:
        return redirect('fridge_create')
    return render(request, 'fridge_list/fridge_list.html',
                  {'page_title': 'Overview of fridge lists', 'fridgeLists': fridgeLists})


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


def delete_fridge(request, **kwargs):
    fridge = FridgeList.objects.get(pk=kwargs['pk'])
    fridge.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def get_fridge_entries(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    items = FridgeEntry.objects.filter(fridgeList=fridge.id)
    if len(items) == 0:
        return redirect('item_create', fridgePk=fridge.id)
    return render(request, 'fridge.html',
                  {'page_title': f'Currently stored in {fridge.title}', 'fridgeEntries': items, 'fridgeId': fridge.id})


def edit_fridge_entry(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    if 'itemPk' in kwargs:
        itemPk = kwargs['itemPk']
    else:
        itemPk = None
    if itemPk:
        fridgeEntry = FridgeEntry.objects.get(pk=itemPk)
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
    return render(request, "edit_fridge_item.html",
                  {'page_title': 'Edit fridge item', 'form': form, 'fridgePk': fridge.id})


def delete_item(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    item = FridgeEntry.objects.get(id=kwargs['itemPk'])
    item.delete()
    return redirect('fridge_items', fridgePk=fridge.id)


def get_shopping_entries(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    items = BuyListEntry.objects.filter(fridgeList=fridge.id)
    if len(items) == 0:
        return redirect('shop_item_create', fridgePk=fridge.id)
    return render(request, 'buylist/shopping_list.html',
                  {'page_title': f'Currently needed for {fridge.title}', 'shoppingEntries': items,
                   'fridgeId': fridge.id})


def edit_shop_entry(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    if 'itemPk' in kwargs:
        itemPk = kwargs['itemPk']
    else:
        itemPk = None
    if itemPk:
        shopEntry = BuyListEntry.objects.get(pk=itemPk)
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


def delete_shopping_item(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    item = BuyListEntry.objects.get(id=kwargs['itemPk'])
    item.delete()
    return redirect('shop_items', fridgePk=fridge.id)


def add_entry_to_fridge(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    item = BuyListEntry.objects.get(id=kwargs['itemPk'])
    item_data = {
        'title': item.title,
        'category': item.category,
        'quantity': item.quantity,
        'quantityType': item.quantityType
    }
    if request.method == 'POST':
        form = FridgeEntryForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.fridgeList = fridge
            new_item.save()
            messages.success(request, 'Shopping list entry moved to fridge!')
            return delete_shopping_item(request, **kwargs)
    else:
        form = FridgeEntryForm(initial=item_data)
    return render(request, "edit_fridge_item.html",
                  {'page_title': 'Edit fridge item', 'form': form})


def add_entry_to_shopping_list(request, **kwargs):
    fridge = FridgeList.objects.get(id=kwargs['fridgePk'])
    item = FridgeEntry.objects.get(id=kwargs['itemPk'])
    item_data = {
        'title': item.title,
        'category': item.category,
        'quantity': item.quantity,
        'quantityType': item.quantityType
    }
    if request.method == 'POST':
        form = BuyListEntryForm(request.POST)
        new_item = form.save(commit=False)
        new_item.fridgeList = fridge
        new_item.save()
        messages.success(request, 'Added to shopping list!')
    return redirect('fridge_items', fridgePk=fridge.id)
