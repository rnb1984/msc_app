from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pizza_ml.models import Pizza, Ingredient, UserPreferance, UserProfile
from learn.pairs import Pairs

# For the RESTFUL API
from rest_framework import generics
from pizza_ml.serializers import PizzaSerializer, IngredientSerializer, UserProfileSerializer, UserPreferanceSerializer


"""
!! TO DO !!
# All views
- index

- details
-- get_details_form

- pizza_choice
-- is_details
-- store_details
-- get_pairs
-- get_pizzas

- predict_pizza
-- is_data
-- pass_data_to_model
-- is_pred
-- get_pizza
"""

# DEFINE FUNCTION !!!
def index(request):
    pizzas = Pizza.objects.all().order_by('index')
    ingredients = Ingredient.objects.all().order_by('index')
    # get_object_or_404(klass, *args, **kwargs)
    context_dict = { 'pizzas' : pizzas, 'ingredients':ingredients }
    return render(request, 'pizza_ml/index.html', context_dict)

# DEFINE FUNCTION !!!
def details(request):
    #form = FormFunction()
    variable = 'welcome'
    context_dict = { 'name' : variable }
    return render(request, 'templates/details.html', context_dict)


# DEFINE FUNCTION !!!
def pizza_choice(request):
    pair = Pairs()
    
    # set up a 30 item training from the 5th indexed pizza item
    pair.set_train(5)
    pair.set_sub()
    
    # set up 4 training rounds with a training set with a controlled sub set of 10
    comparisions = []
    comparisions.append(10)
    comparisions.append(15)
    comparisions.append(15)
    comparisions.append(20)
    pair.set_pairs(4,comparisions)
    
    data = pair.get_dict_comparisions()
    pizza_left =[]
    pizza_right=[]
    print "pair for JSON", data, len(data)
    for index in data:
        pairs = pair.get_pairs(index)
        try:
            pizza_left.append(Pizza.objects.get(index = pairs[0]))
            pizza_right.append(Pizza.objects.get(index = pairs[1]))
        except Pizza.DoesNotExist:
            print "didn't exist"
            
    context_dict= {'left':pizza_left, 'right': pizza_right}
    print 'context_dict: ' , context_dict

    #return JsonResponse(data)
    return render(request, 'pizza_ml/index_test.html', context_dict)


# DEFINE FUNCTION !!!
def predict_pizza(request, date_param):
    # Example jason from BB
    data = {
        'calendar' : 'example',
        'month_string' : 'example',
        'day_string' : 'example',
        'prev_hidden' : 'example',
    }
    return JsonResponse(data)

# API view

class PizzaList(generics.ListCreateAPIView):
    
    queryset = Pizza.objects.all().order_by('name')
    serializer_class = PizzaSerializer


class IngredientList(generics.ListCreateAPIView):
    
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

   
class UserProfileList(generics.ListCreateAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserPreferanceView(generics.RetrieveUpdateAPIView):
    
    queryset = UserProfile.objects.all()
    serializer_class = UserPreferanceSerializer
    
