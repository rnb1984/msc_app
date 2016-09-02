#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza_face_project.settings')

import django
django.setup()

import json
import urllib
import urllib2
from datetime import date

from pizza_ml.models import Pizza, Ingredient

# classes to set up matrix and index items
from indexList import IndexList
from pizzaMatrix import PizzaMatrix
import csv

# glodal vars to help populate database of pizzas
Num_of_Pizzas = 53
pizzaIndex = IndexList()
ingrdIndex = IndexList()
pizzas = PizzaMatrix()

def populate():
  # populate database with pizzas and set up matrix
  with open('pizza_toppings.csv', 'rb') as csvfile:
      ingr_file = csv.reader(csvfile, delimiter=',')
      for ingr in ingr_file:
          if ingr[0] == 'ingredient':
              pass
          else:
              ingrdIndex.add_item(ingr[0])
              added_in = add_ingredients(ingr[0], ingrdIndex.get_index(ingr[0]))

  # create pizza matrix
  pizzas.set_size(ingrdIndex.size(), Num_of_Pizzas)
  
  # populate pizza index, pizza matrix and save all pizzas in database
  with open('pizza_recipe.csv', 'rb') as csvfile:
   ingr_file = csv.reader(csvfile, delimiter=',')
   
   for pizza in ingr_file:
       # add pizza to index and store all data
       if pizza[0] != 'meal name':
        pizzaIndex.add_item(pizza[0])
        pizza_in = pizzaIndex.get_index(pizza[0])
       
        if pizza[2] != 'ingredients':
         # split up the list if character is an alphanumeric character or on a only white space character
         pizza_ingr = ''.join(char for char in pizza[2] if char.isalnum() or char.isspace()).split()
         
         for ingr in pizza_ingr:
          # add ingredients to pizza matrix
          if ingrdIndex.contains_item(ingr):
           pizzas.add_ing(pizza_in,ingrdIndex.get_index(ingr))
          
        added_pizza = add_pizza(pizza[0], pizza[1],pizza_in)

def add_pizza(pizza_name, pizza_image, pizza_index): # populate database with pizzas
  print "pizza added to database, Pizza_name", pizza_name, "pizza_image", pizza_image, "pizza_index_number", pizza_index
  print "ingredients vector"
  p = Pizza.objects.get_or_create(name=pizza_name.lower(), pic= pizza_image , index=pizza_index, ingredients=pizzas.get_ingr(pizza_index) )[0]
  p.save()
  return p

def add_ingredients(ingr_name, ingr_index):  # saves ingredients to database
  i, created = Ingredient.objects.get_or_create(name=ingr_name.lower(),index=ingr_index)
  i.save()
  return i

# Start execution here!
if __name__ == '__main__':
  print "Starting pizza face model test script..."
  populate()