from django.forms import *
from fridge.models import *


class LoginForm(ModelForm):
    class Meta:
        model = Account
        exclude = ()
        labels = {'username': 'Username', 'pw': 'Password'}


class FridgeListForm(ModelForm):
    class Meta:
        model = FridgeList
        exclude = ()
        labels = {'title': 'Title'}


class FridgeEntryForm(ModelForm):
    class Meta:
        model = FridgeEntry
        exclude = ('fridgeList', 'expiringSoon', 'expired')


class BuyListEntryForm(ModelForm):
    class Meta:
        model = BuyListEntry
        exclude = ('fridgeList',)
