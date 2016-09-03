from rest_framework import serializers
from pizza_ml.models import Pizza, Ingredient, UserPreferance

"""
Serializers help create api's for the models
"""

class PizzaSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField('name',
    #    view_name='pizza',
     #   lookup_field='index'
    #)
    
    class Meta:
        model = Pizza
        fields = ('name', 'index', 'pic', 'ingredients', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        #fields = ('name', 'index')
        fields = "__all__"