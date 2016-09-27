from rest_framework import serializers
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance

"""
Serializers
Create api's for the models in a similiar way forms are used
"""

class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','dob','gender','allergies','diet', 'occupation', 'nationality')


class PairPreferanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PairPreferance
        #fields = ( 'id','index','value', 'time', 't_at','browser','scrn_h','scrn_w','scroll_x','scroll_y','pic')
        fields = "__all__"