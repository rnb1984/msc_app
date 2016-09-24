from pairs import Pairs
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance
from pizza_ml.pizza.prep import get_pizza_dict, get_ingredients,get_user_index
import csv

"""
Pairexp
are helpers for setting up experimental pairs for view
- add_pair
- prep_pairs
- get_expone_pair_dict
- get_pair_dict
"""

def add_pair(pair_index, user, exp, pics):
  # Populate database with pairs
  user_id = user.id
  if exp == 1: p = PairPreferance.objects.create(user=user_id, index = pair_index, exp_no=exp, pic=pics)
  else: p = PairPreferance.objects.get_or_create(user=user_id, index = pair_index, exp_no=exp)[0]
  p.save()
  return p
    
def prep_pairs(index,value,time, browser, scrn_h, scrn_w, scroll_x, scroll_y,t_at,date,exp_no,pic ):
    x = {    'index' :index,
            'value':value,
            'time':time,
            'browser':browser,
            'b_h' :scrn_h,
            'b_w' :scrn_w,
            'scr_x':scroll_x,
            'scr_y':scroll_y,
            't_at' :t_at,
            'date' :date,
            'exp' :exp_no,
            'pic' :pic,
             }
    return x

def get_expone_pair_dict(user, pics, exp, rnd):
    pairs = Pairs()
    doc_pairs =[]
    pizzas_index= []
    pizza_left = []
    pizza_right= []
    
    # Get last of predefined pairs for user from experimental design
    #c9Testing:
    with open('pizza_ml/pairset/experiment/experiment_one.csv', 'rb') as expPairs:
        #with open('pizza_face_project/pizza_ml/pairset/experiment/experiment_one.csv', 'rb') as expPairs:
        reader = csv.reader(expPairs)
        for row in reader:
            if int(row[0]) == 100:
                doc_pairs.append(row)
        if rnd%2 !=0:
            doc_pairs.reverse()
        
        if rnd%2 ==0:
            i,j = rnd-1, rnd/2
            doc_pairs[i], doc_pairs[j] = doc_pairs[j], doc_pairs[i]
        
        if rnd%3 ==0:
            doc_pairs.reverse()

        for row in doc_pairs:
                index = pairs.get_index_of_pair(int(row[2]),int(row[-1]))
                pizza_left.append(get_pizza_dict(int(row[2])))
                pizza_right.append(get_pizza_dict(int(row[-1])))
                pair_db = add_pair(index, user, exp, pics)
                pair_db.save()
        
                value = {
                    'id': pair_db.id,
                    'index':index,
                    'value': 2, # can't be 0 or 1 to start with
                    'time':0 
                }
                pizzas_index.append(value)
    expPairs.close()
    return {'lefts':pizza_left, 'rights': pizza_right, 'pairindex': pizzas_index }

def get_pair_dict(user):
    # returns all the experiemental pairs in a dictionary
    user_profile = UserProfile.objects.get(user=user)
    user_index= user_profile.exp_index
    pairs = Pairs()
    
    pizzas_index= []
    pizza_left = []
    pizza_right= []
    
    # Get predefined pairs for user from experimental design
    #c9Testing:
    with open('pizza_ml/pairset/experiment/expdesign_pairs.csv', 'rb') as expPairs:
        #with open('pizza_face_project/pizza_ml/pairset/experiment/expdesign_pairs.csv', 'rb') as expPairs:
        reader = csv.reader(expPairs)
        for row in reader:
            if int(row[0]) == user_index:
                index = pairs.get_index_of_pair(int(row[2]),int(row[-1]))
                pizza_left.append(get_pizza_dict(int(row[2])))
                pizza_right.append(get_pizza_dict(int(row[-1])))
                pair_db = add_pair(index, user, 2, True)
                pair_db.save()
        
                value = {
                    'id': pair_db.id,
                    'index':index,
                    'value': 2, # can't be 0 or 1 to start with
                    'time':0 
                }
                pizzas_index.append(value)
        print len(pizzas_index), user_index
        expPairs.close()
    return {'lefts':pizza_left, 'rights': pizza_right, 'pairindex': pizzas_index }