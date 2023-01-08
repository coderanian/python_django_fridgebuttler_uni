"""fridgebutler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from fridge.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_redirect),
    path('profile/login/', login, name='login'),
    # To be reworked for proper user management
    path('registerTest/', register, name='registrationDummy'),
    path('profile', get_fridge_lists, name='fridge_list'),
    path('profile/fridge/<int:pk>/fridge_edit', edit_fridge_list, name='fridge_edit'),
    path('profile/fridge_create', edit_fridge_list, name='fridge_create'),
    path('profile/fridge/<int:pk>/fridge_delete', delete_fridge, name='delete_fridge'),
    path('profile/fridge/<int:fridgePk>/fridge_items/', get_fridge_entries, name='fridge_items'),
    path(r'profile/fridge/<int:fridgePk>/fridge_items/item_create/', edit_fridge_entry, name='item_create'),
    path('profile/fridge/<int:fridgePk>/fridge_items/<int:itemPk>/item_edit/', edit_fridge_entry, name='item_edit'),
    path('profile/fridge/<int:fridgePk>/fridge_items/<int:itemPk>/item_delete', delete_item, name='item_delete'),
    path('profile/fridge/<int:fridgePk>/fridge_items/<int:itemPk>/item_added/', add_entry_to_shopping_list, name='add_to_shopping_list'),
    path('profile/fridge/<int:fridgePk>/shopping_list', get_shopping_entries, name='shop_items'),
    path('profile/fridge/<int:fridgePk>/shopping_list/item_create/', edit_shop_entry, name='shop_item_create'),
    path('profile/fridge/<int:fridgePk>/shopping_list/<int:itemPk>/item_delete', delete_shopping_item, name='shop_item_delete'),
    path('profile/fridge/<int:fridgePk>/shopping_list/<int:itemPk>/item_edit/', edit_shop_entry, name='shop_item_edit'),
    path('profile/fridge/<int:fridgePk>/shopping_list/<int:itemPk>/item_added/', add_entry_to_fridge, name='add_to_fridge'),
]
