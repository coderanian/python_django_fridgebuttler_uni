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
from django.urls import path
from fridge.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='account'),
    path('account', login, name='account'),
    path('register', register, name='registration'),
    path('fridge_list_overview/', get_fridge_lists, name='fridge_list_overview'),
    path('fridge_list/<int:pk>', get_fridge_entries, name='fridge_list'),
    path('fridge_item', edit_fridge_list, name='fridge_item')
]
