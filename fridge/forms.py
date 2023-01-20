from fridge.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.password_validation import validate_password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    security_question = forms.CharField(max_length=60, label='Who is your favourite superhero?')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'security_question']


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    security_question = forms.CharField(max_length=60, label='Who is your favourite superhero?')
    password1 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password], label='Repeat password')


class FridgeListForm(forms.ModelForm):
    class Meta:
        model = FridgeList
        exclude = ()
        fields = ['title']


class FridgeEntryForm(forms.ModelForm):
    class Meta:
        model = FridgeEntry
        exclude = ('fridgeList', 'expiringSoon', 'expired', 'user',)
        widgets = {
            'expirationDate': DatePickerInput(),
            'openedDate': DatePickerInput()
        }


class BuyListEntryForm(forms.ModelForm):
    class Meta:
        model = BuyListEntry
        exclude = ('fridgeList', 'user',)
