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

from pizza_ml.models import Pizza, Ingredient, UserProfile

# classes to set up matrix and index items
from indexList import IndexList
from pizzaMatrix import PizzaMatrix
import csv

# glodal vars to help populate database of pizzas
Num_of_Pizzas = 51
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
              index_of_ingrd = ingrdIndex.get_index(ingr[0]) # stops plurals being added
              
              # check that ingredents plural version doesn't exist
              try:
                i = Ingredient.objects.get(index = index_of_ingrd)
                if i.name ==  ingrdIndex.get_item(index_of_ingrd) + 's':
                  i.name = ingrdIndex.get_item(index_of_ingrd)
                else:
                  add_ingredients(ingrdIndex.get_item(index_of_ingrd), index_of_ingrd )
              except Exception:
                add_ingredients(ingrdIndex.get_item(index_of_ingrd), index_of_ingrd )
                

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
         pizza_ingr = ''.join(''.join(pizza[2].split('[')).split(']')).split(',')
         for i in range(0, len(pizza_ingr)):
          pizza_ingr[i] = pizza_ingr[i].split("'") #''.join(pizza_ingr[i].split("'"))
          pizza_ingr[i][0] ='.'
          pizza_ingr[i][2] ='.'
          pizza_ingr[i] =''.join(''.join(pizza_ingr[i]).split("."))
         
         for ingr in pizza_ingr:
          # add ingredients to pizza matrix
          if ingrdIndex.contains_item(ingr):
            index_of_ingrd = ingrdIndex.get_index(ingr)
            pizzas.add_ing(pizza_in,index_of_ingrd)
            
            # count ingredients 
            print ingr, 'looking for this', 'index_of_ingrd: ', index_of_ingrd, 
            i = Ingredient.objects.get(index = index_of_ingrd)
            print ingr, ': before i.amount: ', i.amount, 'i.name', i.name
            num = i.amount
            i.amount = num + 1
            i.save()
            print 'i.amount: ', i.amount, 'i.name', i.name
          
        added_pizza = add_pizza(pizza[0], pizza[1],pizza_in)

def add_pizza(pizza_name, pizza_image, pizza_index): # populate database with pizzas
  print "pizza added to database, Pizza_name", pizza_name, "pizza_image", pizza_image, "pizza_index_number", pizza_index
  print "ingredients vector"
  p = Pizza.objects.get_or_create(name=pizza_name.lower(), pic= pizza_image , index=pizza_index, ingredients=pizzas.get_ingr(pizza_index) )[0]
  p.save()
  return p

def add_ingredients(ingr_name, ingr_index):  # saves ingredients to database
  i = Ingredient.objects.get_or_create(name=ingr_name.lower(),index=ingr_index)[0]
  i.save()
  return i
  
def add_userprof(g, a, di):
  u = UserProfile.objects.get_or_create(gender=g, allergies=a, diet=di)[0]
  u.save()
  return u

# Start execution here!
if __name__ == '__main__':
  print "Starting pizza face model test script..."
  populate()