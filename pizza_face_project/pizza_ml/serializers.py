from rest_framework import serializers
from pizza_ml.models import Pizza, Ingredient, UserPreferance

"""
Serializers help create api's for the models
"""

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        #fields = ('name', 'index')
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        #fields = ('name', 'index')
        fields = "__all__"