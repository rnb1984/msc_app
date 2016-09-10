from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance
from learn.pairs import Pairs
from pizza_ml.forms import UserForm

# For the RESTFUL API
from rest_framework import generics
from pizza_ml.serializers import PizzaSerializer, IngredientSerializer, UserProfileSerializer, PairPreferanceSerializer


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


def index(request):
    # Landing page
    pizzas = Pizza.objects.all().order_by('index')
    ingredients = Ingredient.objects.all().order_by('index')

    context_dict = { 'pizzas' : pizzas, 'ingredients':ingredients }
    return render(request, 'pizza_ml/index.html', context_dict)

def details(request):
    # Details page
    
    context_dict = { 'hello' : 'Details please' }
    return render(request, 'pizza_ml/details.html', context_dict)
    
def register(request):
    # Reister for data gathering
    context_dict={}
    # A boolean value for telling the template whether the registration was successful.
    registering = True

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        # valid forms only
        if user_form.is_valid():

            # Save the user's form data to database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            print 'this is a user' , user, 'username', user.username

            # create user profile object with default fields
            profile = UserProfile.objects.get_or_create(user=user)[0] # add to pref pairs

            context_dict = {'form': True}

            return JsonResponse(context_dict)

        # Invalid form or forms - mistakes or something else?
        else:
            return render(request, 'pizza_ml/register.html',{'user_form': user_form, 'errors': user_form.errors})

    # For get request send user form
    else:
        user_form = UserForm()
        context_dict ={'user_form': user_form, 'registering': registering}
    
    return render(request, 'pizza_ml/register.html',context_dict)


def pizza_choice(request):
    # Creates pairs and sends as a 
    # get_object_or_404(klass, *args, **kwargs)
    
    if request.method == 'GET':
        context_dict = { 'welcome' : 'hello world' }
        return render(request, 'pizza_ml/pref-pairs.html', context_dict)
    
    elif request.method == 'POST':
        
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
         
         # create JSON file
         data = pair.get_dict_comparisions()
         pizza_left =[]
         pizza_right=[]
         pizzas_index=[]
         pizzas_rated=[]
         
         for index in data:
            pairs = pair.get_pairs(index)
            pizza_left.append(get_pizza_dict(pairs[0]))
            pizza_right.append(get_pizza_dict(pairs[1]))
            pair_db = add_pair(index)
            value = {
                'id': pair_db.id,
                'index':index ,
                'value': 0
            }
            pizzas_index.append(value)

         context_dict= {'lefts':pizza_left, 'rights': pizza_right, 'pairindex': pizzas_index }
         return JsonResponse(context_dict)


def predict_pizza(request):
    # send back holding page for prediction and calculate ml
    if request.method == 'GET':
        pairs = PairPreferance.objects.all()
        # pass all the pairs to ml
        # prediction to be calculated 
        context_dict = { 'welcome' : 'Ready for your predictiond', 'pairs': pairs }
        return render(request, 'pizza_ml/predict.html', context_dict)
        
    elif request.method == 'POST':
        # on post 
        context_dict= {'prediction': 'prediction_pizza', 'guess': 'yes or no' }
        return JsonResponse(context_dict)
    

# Helpers functions
def get_ingredients(string):
    # parses the vector string from Pizza and returns all ingredients names
    ingredients=[]
    list_of_ingd = string.split(',')
    list_of_ingd.pop(0)
    
    for i in range(0,len(list_of_ingd)):
        list_of_ingd[i] = int(list_of_ingd[i])
        if list_of_ingd[i] == 1:
            try:
                ingd = Ingredient.objects.get(index=i) # get_object_or_404(klass, *args, **kwargs)
                ingredients.append(ingd.name)
            except Ingredient.DoesNotExist:
                print "Ingredient didn't exist"
    return ingredients

def get_pizza_dict(new_index):
    # Reutrns a dictionary of Pizzasto be past as JSON 
    try:
        pizza = Pizza.objects.get(index = new_index)
    except Pizza.DoesNotExist:
        print "didn't exist"
        
    pizza = {
        'index': pizza.index,
        'name': pizza.name,
        'pic': pizza.pic,
        'ingredients' : get_ingredients(pizza.ingredients)
    }
    return pizza
    
def add_pair(pair_index):
  # populate database with pairs
  p = PairPreferance.objects.get_or_create(index=pair_index)[0]
  p.save()
  print 'p', p, 'id', p.id
  return p


# API view
class PizzaList(generics.ListCreateAPIView):
    # returns a list of pizzas
    queryset = Pizza.objects.all().order_by('name')
    serializer_class = PizzaSerializer


class IngredientList(generics.ListCreateAPIView):
    # returns a list of ingredients
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

   
class UserProfileList(generics.ListCreateAPIView):
    # returns a list of profiles
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    # edit a profile depending on a id/pk
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    
class PairPrefLists(generics.ListCreateAPIView):
    # returns a list of pairs
    queryset = PairPreferance.objects.all()
    serializer_class = PairPreferanceSerializer

class PairPrefDetails(generics.RetrieveUpdateDestroyAPIView):
    # edit a pairs depending on a id/pk
    queryset = PairPreferance.objects.all()
    serializer_class = PairPreferanceSerializer    
