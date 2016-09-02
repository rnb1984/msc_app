from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pizza_ml.models import Pizza, Ingredient, UserPreferance, UserProfile

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
    variable = 'welcome'
    context_dict = { 'name' : variable }
    return render(request, 'templates/index.html', context_dict)

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

