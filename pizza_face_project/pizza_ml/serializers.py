from rest_framework import serializers
from pizza_ml.models import Pizza, Ingredient, UserProfile, UserPreferance, PairPreferance

"""
Serializers
Create api's for the models in a similiar way forms are used
"""

class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        #fields = ('name', 'index', 'pic', 'ingredients', 'slug')
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        #fields = ('dob','gender','allergies','diet')
        fields = "__all__"



class PairPreferanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PairPreferance
        fields = ( 'id','index','value')
        #fields = "__all__"
