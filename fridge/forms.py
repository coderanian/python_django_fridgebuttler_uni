from fridge.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FridgeListForm(forms.ModelForm):
    class Meta:
        model = FridgeList
        exclude = ()
        labels = {'title': 'Title'}


class FridgeEntryForm(forms.ModelForm):
    class Meta:
        model = FridgeEntry
        exclude = ('fridgeList', 'expiringSoon', 'expired')


class BuyListEntryForm(forms.ModelForm):
    class Meta:
        model = BuyListEntry
        exclude = ('fridgeList',)
