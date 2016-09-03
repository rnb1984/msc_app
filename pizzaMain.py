from IndexList import IndexList
from PizzaMatrix import PizzaMatrix
import os, csv

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
          store_pizza(pizza[0], pizza[1],pizza_in)
         
         if pizza[2] != 'ingredients':
          # split up the list if character is an alphanumeric character or on a only white space character
          pizza_ingr = ''.join(char for char in pizza[2] if char.isalnum() or char.isspace()).split()
          
          for ingr in pizza_ingr:
           # add ingredients to pizza matrix
           if ingrdIndex.contains_item(ingr):
            pizzas.add_ing(pizza_in,ingrdIndex.get_index(ingr))

def store_pizza(pizza_name, pizza_image, pizza_index):
 # populate database with pizzas
 print "pizza added to database"
 

populate()

print "------------ ingrd indexed ------------ "
print ingrdIndex.index_list
print "----------------------------------------- "


print "------------ pizza indexed ------------"
print pizzaIndex.index_list
print "----------------------------------------- "
print "!!!!!pizza matrix!!!!!!"
print pizzas.Depth
print pizzas.Bredth
for piz in range(pizzaIndex.size()):
 print "------------", pizzaIndex.get_item(piz), "------------"
 print 'this pizza hass all of these toppings '
 for i in range(ingrdIndex.size()):
  if pizzas.Matrix[piz][i] == 1:
   print ' --+', ingrdIndex.get_item(i)
print "-----------------------------------------"