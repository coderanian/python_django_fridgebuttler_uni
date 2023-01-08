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
    path('', login, name='account'),
    path('account', login, name='account'),
    path('register', register, name='registration'),
    path('fridge_list/', get_fridge_lists, name='fridge_list'),
    path('fridge_edit/<int:pk>', edit_fridge_list, name='fridge_edit'),
    path('fridge_edit', edit_fridge_list, name='fridge_create'),
    path('/delete/<int:pk>', delete_fridge, name='delete_fridge'),
    path('<int:fridgePk>/fridge_items/', get_fridge_entries, name='fridge_items'),
    path('/item_create/', edit_fridge_entry, name='item_create'),
    path('item_edit/<int:itemPk>', edit_fridge_entry, name='item_edit'),
]
