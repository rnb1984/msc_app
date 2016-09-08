from django.contrib import admin
from pizza_ml.models import Pizza, Ingredient, UserProfile, UserPreferance, PairPreferance

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Ingredient)
admin.site.register(UserProfile)
admin.site.register(UserPreferance)
admin.site.register(PairPreferance)
