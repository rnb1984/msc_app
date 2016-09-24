from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import json, datetime, time
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
from pizza_ml.serializers import PizzaSerializer, IngredientSerializer, UserProfileSerializer, PairPreferanceSerializer, PairPreferanceDeviceSerializer


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
         user_profile = UserProfile.objects.get(user=user)
         user_index= user_profile.exp_index
         print user_index
         pairs = Pairs()
         
         pizzas_index= []
         pizza_left = []
         pizza_right= []
         
         # Get predefined pairs for user from experimental design
         #c9Testing:
         with open('pizza_ml/learn/experiment/expdesign_pairs.csv', 'rb') as expPairs:
         #with open('pizza_face_project/pizza_ml/learn/experiment/expdesign_pairs.csv', 'rb') as expPairs:
            reader = csv.reader(expPairs)
            for row in reader:
                if int(row[0]) == user_index:
                    index = pairs.get_index_of_pair(int(row[2]),int(row[-1]))
                    pizza_left.append(get_pizza_dict(int(row[2])))
                    pizza_right.append(get_pizza_dict(int(row[-1])))
                    pair_db = add_pair(index, user)
                    pair_db.exp_no = 2
                    pair_db.save()

                    value = {
                        'id': pair_db.id,
                        'index':index,
                        'value': 2, # can't be 0 or 1 to start with
                        'time':0 
                    }
                    pizzas_index.append(value)
                    
         expPairs.close()
         
         # create JSON file
         context_dict= {'lefts':pizza_left, 'rights': pizza_right, 'pairindex': pizzas_index }
         return JsonResponse(context_dict)

# Last page
@login_required
def results(request):
    # send back holding page for prediction and calculate ml
    if request.method == 'GET':
        userd = UserProfile.objects.get( user= request.user)
        # pass all the pairs to ml # prediction to be calculated
        context_dict = { 'title' : 'Congratulations', 'details' :userd }
        return render(request, 'pizza_ml/predict.html', context_dict)
    
    elif request.method == 'POST':
        context_dict={'reply':' '}
        # post should have returned a yes or no answer
        pairs = PairPreferance.objects.all()
        user= request.user
        answer = json.loads(request.body)
        answer =  answer['answer']
        
        # make sure it is the correct data
        if answer == 'yes' or answer == 'no':
            user_pro = UserProfile.objects.get(user=user)
            pairs = PairPreferance.objects.filter(user=user.id)
            a =[]
            for p in pairs:
                x = {
                    'index' : p.index,
                    'value':p.value,
                    'time': p.time,
                    'browser': p.browser,
                    'b_h' : p.scrn_h,
                    'b_w' : p.scrn_w,
                    'scr_x': p.scroll_x,
                    'scr_y': p.scroll_y,
                    't_at' : p.t_at,
                    'date' : p.date,
                    'exp' : p.exp_no,
                    'pic' : p.pic,
                     }
                a.append(x)
            pairs= a
            doc_new=[]
            row=[]
            row.append(user.username)
            row.append(user.email)
            row.append(user_pro.dob)
            row.append(user_pro.gender)
            row.append(user_pro.allergies)
            row.append(user_pro.diet)
            row.append(user_pro.occupation)
            row.append(user_pro.nationality)
            row.append(pairs)
            row.append(answer)
            row.append(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            
            # save all info to a csv file
            doc_new.append(row)
            save_to_csv(doc_new)
            
            if answer == 'no': context_dict['reply'] = "Thank you. You will not recieve an email with a pizza prediction."
            elif answer == 'yes': context_dict['reply'] = 'Thank you! You will recieve an email with your prediction on this address ' + user.email
        else:
            context_dict={'reply':'Sorry we did not get an answer from you, please email 2155569b@student.gla.ac.uk'}
        return JsonResponse(context_dict)


"""
Helpers
- get_ingredients
- get_pizza_dict
- get_user_index
- add_pair
- save_to_csv
"""
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
        print "Pizza didn't exist"
        
    pizza = {
        'index': pizza.index,
        'name': pizza.name,
        'pic': pizza.pic,
        'ingredients' : get_ingredients(pizza.ingredients)
    }
    return pizza
    
def get_user_index():
    # returns unused user index from experiment
    new_index= 1
    all_users = UserProfile.objects.all()
    
    if len(all_users) <1:
        return new_index
    else:
        new_index=len(all_users)
        return new_index

def add_pair(pair_index, user):
  # Populate database with pairs
  user_id = user.id
  p = PairPreferance.objects.get_or_create(user=user_id, index = pair_index)[0]
  p.save()
  return p

def save_to_csv(doc_new):
    # Saves all results on exisiting file
    doc_in = []
    #c9Testing:
    with open('pizza_ml/results/results.csv', 'rb') as inText:
    #with open('pizza_face_project/pizza_ml/results/results.csv', 'rb') as inText:
        reader = csv.reader(inText)
        for row in reader:
            doc_in.append(row)
    inText.close()
    
    for doc in doc_new:
        doc_in.append(doc)
    
    # Store all information in a csv file
    #c9Testing:
    with open('pizza_ml/results/results.csv', 'w') as outText:
    #with open("pizza_face_project/pizza_ml/results/results.csv", "w") as outText:
        writer = csv.writer(outText, delimiter=",")
        writer.writerow(doc_in[0])
    
        for i in range(1,len(doc_in)):
            out_doc = doc_in[i]

            writer.writerow(out_doc)
    outText.close()


"""
API Custom
- Current User details
- Nationality dictionary
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
    context_dict = {}
    nat_list=[]
    #c9Testing:
    with open('pizza_ml/data/nations.csv', 'rb') as nat:
    #with open('pizza_face_project/pizza_ml/data/nations.csv', 'rb') as nat:
        reader = csv.reader(nat)
        for row in reader:
            country = {
                row[0] : row[1],
                row[2] : row[3]
            }
            nat_list.append(country)
    context_dict = { 'nationality' :nat_list}
    return JsonResponse(context_dict)

# Current Results
def curr_results(request):
    context_dict = {}
    res_list=[]
    #c9Testing:
    with open('pizza_ml/results/results.csv', 'rb') as res:
    #with open('pizza_face_project/pizza_ml/results/results.csv', 'rb') as res:
        reader = csv.reader(res)
        for row in reader:
            print len(row), ' is the size and this is the row :', row
            users = {
                'username': row[0],
                'email' : row[1],
                'dob' : row[2],
                'gender' : row[3],
                'allergies': row[4],
                'diet': row[5],
                'occupation': row[6],
                'nationality': row[7],
                'pairs': row[8],
                'permission' : row[-2],
                'completed time' : row[-1],
            }
            res_list.append(users)
    context_dict = { 'results' :res_list}
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

class PairPrefDevice(generics.RetrieveUpdateDestroyAPIView):
    # edit the users details for every pair prefance taken
    queryset = PairPreferance.objects.all()
    serializer_class = PairPreferanceDeviceSerializer

