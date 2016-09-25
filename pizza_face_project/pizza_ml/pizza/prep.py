from pizza_ml.models import Pizza, Ingredient, UserProfile

"""
Prep
are helper functions for preparing pizza objects for views
- get_ingredients
- get_pizza_dict
- get_user_index
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
    # Reutrns a dictionary of Pizzas to be past as JSON
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

