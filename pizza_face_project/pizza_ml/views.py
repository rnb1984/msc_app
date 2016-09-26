from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import json, datetime, time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance
from pizza_ml.pairset import pairexp
from pizza_ml.results import result
from pizza_ml.pizza.prep import get_pizza_dict, get_ingredients,get_user_index
from pizza_ml.forms import UserForm

# For the RESTFUL API
from rest_framework import generics
from pizza_ml.serializers import PizzaSerializer, IngredientSerializer, UserProfileSerializer, PairPreferanceSerializer

# Exp one
from random import randint

"""
Views
- Landing page
- Register page
- Login page
- Log out
- restrictions
- Deails page
- Trainging page
- Pizza choices page
- Last page

Helpers
Custom API's
API REST
"""

# Landing page
def index(request):
    # Landing page
    pizzas = Pizza.objects.all().order_by('index')
    ingredients = Ingredient.objects.all().order_by('index')

    context_dict = { 'title' : 'Welcome','pizzas' : pizzas, 'ingredients':ingredients }
    return render(request, 'pizza_ml/index.html', context_dict)
 
# Register page  
def register(request):
    # Reister for data gathering
    context_dict={}
    # A boolean value for telling the template whether the registration was successful
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

            # create user profile object with userprofile details and user id
            profile = UserProfile.objects.get_or_create(user=user)[0] # add to pref pairs
            profile.exp_index = get_user_index()
            profile.save()
            
            # feed back
            context_dict = {'form': registering, 'id': profile.id}
            return HttpResponseRedirect('/login/')

        # Invalid form or forms - mistakes or something else?
        else:
            return render(request, 'pizza_ml/user/register.html',{'user_form': user_form, 'errors': user_form.errors})

    # For get request send user form
    else:
        user_form = UserForm()
        context_dict ={ 'title' : 'Register' ,'user_form': user_form, 'registering': registering}
    
    return render(request, 'pizza_ml/user/register.html', context_dict)

# Login page
def user_login(request):

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use username/password to find User object
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # If the account is valid or already login, go back to home page
                login(request, user)
                return HttpResponseRedirect('/details/')
            else:
                # Not logged in
                return HttpResponse("Your are not logged in.")
        else:
            # No user found
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        # not logged in so register
        return render(request, 'pizza_ml/user/login.html', {'title' : 'Login'})

# Log out
@login_required
def user_logout(request):
    # Uses django defaults to log out 
    logout(request)
    return HttpResponseRedirect('/pizzaface/')

@login_required
def restricted(request):
    return HttpResponse("MINKA!! You are not logged in")

# Deails page
@login_required
def details(request):
    # Details page
    context_dict = {'title' : 'Details', 'id' : request.user.id }
    return render(request, 'pizza_ml/user/details.html', context_dict)

# Trainging page
@login_required
def train(request):
    if request.method == 'GET':
        print 'got here GET'
        context_dict = { 'title' : 'Training' }
        return render(request, 'pizza_ml/pref-pairs.html', context_dict)
        
    elif request.method == 'POST':
         # create 3 pairs for user to train on
         pizza_left= []
         pizza_right=[]
         pizza_pairs= [{ 'l': 2, 'r': 3 },{ 'l': 4, 'r': 35 },{ 'l': 14, 'r': 5 }]
         value = {'id': 99999999999,'index':99999999,'value': 2, 'time':0  }  # for training 
         pizza_index = []
         
         # add pizza details
         for pair in pizza_pairs:
             pizza_left.append(get_pizza_dict(pair['l']))
             pizza_right.append(get_pizza_dict(pair['r']))
             pizza_index.append(value)
             
         context_dict= {'lefts':pizza_left, 'rights': pizza_right, 'pairindex': pizza_index }
         return JsonResponse(context_dict)

# Pizza choices page
@login_required
def pizza_choice(request):
    # Creates pairs and sends as a 
    if request.method == 'GET':
        # title differentates comands on client side
        context_dict = { 'title' : 'Choices' } 
        return render(request, 'pizza_ml/pref-pairs.html', context_dict)
    
    elif request.method == 'POST':
         # Post back assigned pairs from experiment design
         user = request.user
         # create JSON file
         context_dict= pairexp.get_pair_dict(user)
         return JsonResponse(context_dict)

# Last page
@login_required
def results(request):
    # send back holding page for prediction and calculate ml
    if request.method == 'GET':
        userd = UserProfile.objects.get( user= request.user)
        # pass all the pairs to ml # prediction to be calculated
        context_dict = { 'title' : 'Congratulations', 'details' :userd }
        return render(request, 'pizza_ml/user/permissions.html', context_dict)
    
    elif request.method == 'POST':
        context_dict={'reply':' '}
        # post should have returned a yes or no answer
        user= request.user
        answer = json.loads(request.body)
        answer =  answer['answer']
        
        # make sure it is the correct data
        if answer == 'yes' or answer == 'no':
            # save all info to a csv file
            result.save_user_to_csv(user, 'results', answer)
            # save all pairs
            result.save_user_pairs_to_csv(user, 2)
            
            if answer == 'no': context_dict['reply'] = "Thank you. You will not recieve an email with a pizza prediction."
            elif answer == 'yes':
                result.save_emails(user.username, user.email)
                context_dict['reply'] = 'Thank you! You will recieve an email with your prediction on this address ' + user.email
        else:
            context_dict={'reply':'Sorry we did not get an answer from you, please email 2155569b@student.gla.ac.uk'}
        return JsonResponse(context_dict)


"""
API Custom
- Current User details
- Nationality dictionary
- Current Results
"""

# Current User details
@login_required
def current_user(request):
    # Posts user information
    user_profile = UserProfile.objects.get(user=request.user)
    data = { 'id' : user_profile.id , "dob": user_profile.dob,"gender": user_profile.gender,"allergies": user_profile.allergies,"diet": user_profile.diet, "nationality" : user_profile.nationality, "occupation" : user_profile.occupation }
    return JsonResponse(data)

# Nationality dictionary
def nationality(request):
    context_dict = result.get_nationality()
    return JsonResponse(context_dict)

# Current Results user
def curr_results(request):
    context_dict = result.get_results_dict('results',2)
    return JsonResponse(context_dict)

# Current Results pairs
def curr_results_pairs(request):
    context_dict = result.get_user_all_pairs(2)
    return JsonResponse(context_dict)

# Current Results users
def curr_results_users(request):
    context_dict = result.get_user_dict('email')
    return JsonResponse(context_dict)

"""
Experiement One
- exp_one
- exp_one_pairs
- start
- finish
- exp_results
"""
# Intro Experiment One Page
def exp_one(request):
    context_dict = { 'title' : 'Welcome to Experiement One'}
    return render(request, 'pizza_ml/expone/expone_home.html', context_dict)

# Experiment One Pairs Page
@login_required
def exp_one_pairs(request):
    if request.method == 'GET':
        context_dict = { 'title' : 'Experiement One'}
        return render(request, 'pizza_ml/expone/pref-noimage.html', context_dict)
    elif request.method == 'POST':
        user = request.user
        # random number in index of 20 to create random order
        rn = randint(0,20)
        pics= pairexp.get_expone_pair_dict(user, True, 1,rn)

        # make sure it is not the same as first index
        if rn%2 !=0 or rn == 10:
            rn = rn+1
        else:
            rn = 20 - rn
        nopics = pairexp.get_expone_pair_dict(user, False, 1,rn)

        # create JSON file
        context_dict= {'pics':pics, 'nopics': nopics}
        return JsonResponse(context_dict)

# Deails page
@login_required
def exp_one_details(request):
    # Details page
    context_dict = {'title' : 'Experment Details', 'id' : request.user.id }
    return render(request, 'pizza_ml/user/details.html', context_dict)

# Trainging page
@login_required
def exp_one_train(request):
    context_dict = { 'title' : 'TrainEX' }
    return render(request, 'pizza_ml/pref-pairs.html', context_dict)

# Start API
def start(request):
    # API that returns a random integer to indecate wether the user will be given images or not to start with
    data={'start': randint(1,10) }
    return JsonResponse(data)

# Final Page
@login_required
def finish(request):
    if request.method == 'GET':
        userd = UserProfile.objects.get( user= request.user)
        context_dict = { 'title' : 'Congratulations', 'details' :userd }
        return render(request, 'pizza_ml/expone/expone-permissions.html', context_dict)
    
    elif request.method == 'POST':
        context_dict={'reply':' '}
        # post should have returned a yes or no answer
        user= request.user
        answer = json.loads(request.body)
        answer =  answer['answer']
        
        # make sure it is the correct data
        if answer == 'yes' or answer == 'no':
            user_pro = UserProfile.objects.get(user=user)
            # save all users details to exp_one doc
            result.save_user_to_csv(user, 'exp_one', answer)
            # save all pairs in a their own doc
            result.save_user_pairs_to_csv(user, 1)
            
            if answer == 'no': context_dict['reply'] = "Thank you. You will not recieve an email with a pizza prediction."
            elif answer == 'yes':
                result.save_emails(user.username, user.email)
                context_dict['reply'] = 'Thank you! You will recieve an email with your prediction on this address ' + user.email
        else:
            context_dict={'reply':'Sorry we did not get an answer from you, please email 2155569b@student.gla.ac.uk'}
        return JsonResponse(context_dict)

# API exp results user
def exp_results(request):
    context_dict = result.get_results_dict('exp_one', 1)
    return JsonResponse(context_dict)

# API exp results pairs
def exp_results_pairs(request):
    context_dict = result.get_user_all_pairs(1)
    return JsonResponse(context_dict)

"""
API REST
- Pizza List
- Ingredient List
- UserProfile List
- UserProfile Details
- PairPref Lists
- PairPref Details
"""
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


