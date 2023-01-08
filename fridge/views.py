from django.shortcuts import render
from fridge.models import *
from fridge.forms import *
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView


# Create your views here.
def login(request):
    form = LoginForm()
    return render(request, "account.html", {'page_title': 'Login into your account', 'form': form})


def register(request):
    account = Account()
    form = LoginForm(request.POST, instance=account)
    if form.is_valid():
        form.save()
        messages.success(request, 'Registration completed!')
        return HttpResponseRedirect(reverse_lazy('account'))
    return render(request, "fridge_list/../templates/register.html", {'page_title': 'Registration', 'form': form})


def get_fridge_lists(request):
    fridgeLists = FridgeList.objects.all()
    # Redirect to new list creation if no lists added
    if len(fridgeLists) == 0:
        return redirect('fridge_create')
    return render(request, 'fridge_list/fridge_list.html', {'page_title': 'Overview of fridge lists', 'fridgeLists': fridgeLists})


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
            return HttpResponseRedirect(reverse_lazy('fridge_list'))
    else:
        form = FridgeListForm(instance=fridgeList)
    return render(request, "fridge_list/edit_fridge.html", {'page_title': 'Edit fridge list', 'form': form})


def delete_fridge(request, pk=None):
    fridge = FridgeList.objects.get(pk=pk)
    fridge.delete()
    return HttpResponseRedirect(reverse_lazy('fridge_list'))

def get_fridge_entries(request, pk=None):
    if pk:
        fridgeEntries = FridgeEntry.objects.all()
        if len(fridgeEntries) == 0:
            return redirect('fridge_item')
    return render(request, 'fridge.html', {'page_title': 'Fridge List DUMMY'})


def edit_fridge_entry(request, pk=None):
    if pk:
        fridgeEntry = FridgeEntry.objects.get(pk=pk)
    else:
        fridgeEntry = FridgeEntry()
    if request.method == 'POST':
        form = FridgeEntryForm(request.POST, instance=fridgeEntry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fridge entry saved!')
            return HttpResponseRedirect(reverse_lazy('fridge_list'))
    else:
        form = FridgeListForm(instance=fridgeEntry)
    return render(request, "edit_fridge_item.html", {'page_title': 'Edit fridge item', 'form': form})
