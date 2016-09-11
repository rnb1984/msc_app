from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance
from learn.pairs import Pairs
from pizza_ml.forms import UserForm
import csv

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
            print 'this is a user' , user, 'username', user.username

            # create user profile object with userprofile details and user id
            profile = UserProfile.objects.get_or_create(user=user)[0] # add to pref pairs
            profile.save()
            
            # feed back
            context_dict = {'form': registering, 'id': profile.id}
            return HttpResponseRedirect('/login/')

        # Invalid form or forms - mistakes or something else?
        else:
            return render(request, 'pizza_ml/register.html',{'user_form': user_form, 'errors': user_form.errors})

    # For get request send user form
    else:
        user_form = UserForm()
        context_dict ={'user_form': user_form, 'registering': registering}
    
    return render(request, 'pizza_ml/register.html',context_dict)
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
        return render(request, 'pizza_ml/user/login.html', {})

@login_required
def user_logout(request):
    # Uses django defaults to log out 
    logout(request)
    return HttpResponseRedirect('/pizzaface/')

@login_required
def restricted(request):
    return HttpResponse("You are logged in")

# Posts user id
def current_user(request):
    user_profile = UserProfile.objects.get(user=request.user)
    data = { 'id' : user_profile.id , "dob": user_profile.dob,"gender": user_profile.gender,"allergies": user_profile.allergies,"diet": user_profile.diet}
    return JsonResponse(data)

# Deails page
def details(request):
    # Details page
    context_dict = { 'id' : request.user.id }
    return render(request, 'pizza_ml/details.html', context_dict)

# Pizza choices page
def pizza_choice(request):
    # Creates pairs and sends as a 
    print 'got here with', request.method
    if request.method == 'GET':
        context_dict = { 'welcome' : 'hello world' }
        return render(request, 'pizza_ml/pref-pairs.html', context_dict)
    
    elif request.method == 'POST':
         print 'in Post'
         user = request.user
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
             # from classget the index and create a pairobject
            pairs = pair.get_pairs(index)
            pizza_left.append(get_pizza_dict(pairs[0]))
            pizza_right.append(get_pizza_dict(pairs[1]))
            pair_db = add_pair(index, user)
            value = {
                'id': pair_db.id,
                'index':index ,
                'value': 0
            }
            pizzas_index.append(value)
         print 'pizza_left', pizza_left, 'pizza_right', pizza_right
         context_dict= {'lefts':pizza_left, 'rights': pizza_right, 'pairindex': pizzas_index }
         return JsonResponse(context_dict)

# Last page
def results(request):
    # send back holding page for prediction and calculate ml
    if request.method == 'GET':
        pairs = PairPreferance.objects.all()
        # pass all the pairs to ml # prediction to be calculated
        user= request.user
        user_pro = UserProfile.objects.get(user=user)
        pairs = PairPreferance.objects.filter(user=user.id)
        a =[]
        for p in pairs:
            x = {'index' : p.index, 'value':p.value}
            a.append(x)
        print a
        pairs= a
        doc_new=[]
        row=[]
        username= user.username
        email= user.email
        dob = user_pro.dob
        gender = user_pro.gender
        allergies = user_pro.allergies
        diet = user_pro.diet
        row.append(username)
        row.append(email)
        row.append(dob)
        row.append(gender)
        row.append(allergies)
        row.append(diet)
        row.append(pairs)
        # save all info to a csv file
        doc_new.append(row)
        save_to_csv(doc_new)
        # feedback
        context_dict = { 'welcome' : 'Ready for your predictiond', 'pairs': pairs }
        return render(request, 'pizza_ml/predict.html', context_dict)



    

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
    
def add_pair(pair_index, user):
  # populate database with pairs
  user_id = user.id
  p = PairPreferance.objects.get_or_create(index = pair_index)[0]
  p.user=user_id
  p.save()
  print 'new', p
  print 'p', p, 'id', p.id
  return p

def save_to_csv(doc_new):
    doc_in = []
    # Open and read
    with open('pizza_ml/results/results.csv', 'rb') as inText:
        reader = csv.reader(inText)
        for row in reader:
            doc_in.append(row)
    inText.close()
    
    for doc in doc_new:
        doc_in.append(doc)
    
    # Store all information in a csv file    
    with open("pizza_ml/results/results.csv", "w") as outText:
        writer = csv.writer(outText, delimiter=",")
        writer.writerow(doc_in[0])
    
        for i in range(1,len(doc_in)):
            out_doc = doc_in[i]

            writer.writerow(out_doc)
    outText.close()




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
