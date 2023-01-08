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


def edit_fridge_list(request, pk=None):
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


def delete_fridge(request, pk=None):
    fridge = FridgeList.objects.get(pk=pk)
    fridge.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def get_fridge_entries(request, fridgePk=None):
    fridge = FridgeList.objects.get(pk=fridgePk)
    items = fridge.fridge.all()
    if len(items) == 0:
        return redirect('item_create', fridgePk=fridgePk)
    return render(request, 'fridge_items', {'page_title': f'Currently stored in {fridge.title}', 'fridgeEntries': items})


def edit_fridge_entry(request, itemPk=None, fridgePk=None):
    if itemPk:
        fridgeEntry = FridgeEntry.objects.get(pk=itemPk)
    else:
        fridgeEntry = FridgeEntry()
    if request.method == 'POST':
        form = FridgeEntryForm(request.POST, instance=fridgeEntry)
        if form.is_valid():
            #newItem = form.save(commit=False)
            #newItem.fridgeList = FridgeList.objects.get(pk=fridgePk)
            newItem.save()
            messages.success(request, 'Fridge entry saved!')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = FridgeEntryForm(instance=fridgeEntry)
    return render(request, "edit_fridge_item.html", {'page_title': 'Edit fridge item', 'form': form})


def delete_item(request, pkItem=None):
    item = FridgeEntry.objects.get(pk=pkItem)
    item.delete()
    return HttpResponseRedirect(reverse_lazy('fridge_items'))


