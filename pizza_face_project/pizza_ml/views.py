from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pizza_ml.models import Pizza, Ingredient, UserPreferance, UserProfile

# For the RESTFUL API
#from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pizza_ml.serializers import PizzaSerializer, IngredientSerializer


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
def pizza_choice(request, date_param):
    # Example jason from BB
    data = {
        'calendar' : 'example',
        'month_string' : 'example',
        'day_string' : 'example',
        'prev_hidden' : 'example',
    }
    return JsonResponse(data)


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
# pizzas/
#class PizzaList(viewsets.ModelViewSet):
    #queryset = Pizza.objects.all().order_by('index')
    #serializer_class = PizzaSerializer
    
class PizzaList(APIView):
    
    def get(self, request):
        pizza = Pizza.objects.all().order_by('index')
        serializer = PizzaSerializer(pizza, many=True)
        return Response(serializer.data)
        
    def post(self):
        pass
    
class IngredientList(APIView):
    
    def get(self, request):
        ingrd = Ingredient.objects.all().order_by('amount')
        serializer = IngredientSerializer(ingrd, many=True)
        return Response(serializer.data)
        
    def post(self):
        pass