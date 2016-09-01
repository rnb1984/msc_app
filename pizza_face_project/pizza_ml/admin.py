from django.contrib import admin
from pizza_ml.models import Pizza, Ingredients, UserProfile, UserPreferance

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Ingredients)
admin.site.register(UserProfile)
admin.site.register(UserPreferance)
