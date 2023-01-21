# Fridgebutler

## Autors

- Konstantin Kuklin
- Lasse Broer

Für Technische Hochschule Brandenburg 2022

## Introduction

This application helps the users to manage their fridges and shopping lists.
Each user can create and multiple fridge lists. Each fridge lists has associated items overview and dedicated shopping
list.

## Required packages

Please refer to requirements.txt for required packages.

- asgiref==3.6.0
- beautifulsoup4==4.11.1
- Django==4.1.5
- django-bootstrap-datepicker-plus==5.0.3
- django-bootstrap4==22.3
- fontawesomefree==6.2.1
- pydantic==1.10.4
- soupsieve==2.3.2.post1
- sqlparse==0.4.3
- typing_extensions==4.4.0
- tzdata==2022.7

## What is this project?

- README.MD:  
  Project information

- templates:  
  Folder containing html templates for each view. Templates generate html during runtime.

- static:  
  static files needed served to templates during runtime

- fridgebutler:  
  contains application settings and url patterns

- fridge:  
  contains database model, forms generation, function that takes a web request and returns a web response

- db.sqlite3:  
  SQLite database file

## Features

1. User can create an account and update password
2. Logged user can freely navigate between different views via button press
3. Logged user can create and edit "fridges"
4. Logged user can create and edit items in each fridge
5. Logged user can sort items in fridge by expiration date or category
6. Logged user can delete, edit or add item from fridge to shopping list
7. If item's category is a perishable good, user receives visual notification about expired (red) and soon to expire (
   orange) goods
8. If there are expired items in the fridge, user receives notification with overview when accessing each time accessing
   the fridge until items are removed from it.
9. Each fridge has its own shopping list
10. Logged user can either access shopping list of the fridge (from fridge view) or consoldiated shopping list (from
   fridges list view)
11. Logged user can create, update, delete and see details of items of the shopping list
12. Logged user can mark item as bought to delete it from shopping list and add it to fridge list