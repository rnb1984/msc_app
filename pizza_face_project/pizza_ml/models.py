from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.core.validators import validate_email
from django.template.defaultfilters import slugify
from datetime import date

"""
- Pizza
- Ingredients
- UserProfile
- UserPreferance
"""
# Change to integers !!!
GENDER_CHOICES = (
    ('U', 'Undisclosed'),
    ('F', 'Female'),
    ('M', 'Male'),
)

# DEFINE MODEL !!!
class UserProfile(models.Model):
    """
	UserProfile
	- Stores user details of participance
	to be used in post evaluation.
	"""
	
    user = models.OneToOneField(User)
    dob = models.IntegerField(default=0)
    gender = models.CharField(default="U", max_length=1, choices=GENDER_CHOICES)
    allergies = models.CharField(default="0", max_length=128)
    diet = models.CharField(default="0", max_length=128)
    occupation = models.IntegerField(default=0)
    
    """
	UserPreferance
	- Stores fk to pizza pair index, with 0 or 1 rating, used in comparsisons
	- Stores latest prediction as pizza index integer
	- Stores boolean for if prediction was true or false
	"""
	
	# Current prediction = int    predict = models.IntegerField(default=0)			!!
	# Prediction correct = boolean   correct = models.BooleanField(default=False)	!!
    slug = models.SlugField()

    def save(self, *args, **kwargs):
         self.slug = slugify(self.user.username)
         super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
    	return self.user.username
        

class Pizza(models.Model):
	"""
	Pizza
	- Stores name of pizza, pic of pizza, index pizza is on matrix of pizza and a feature vecture of ingredients
	"""

	name = models.CharField(max_length=128) 
	index = models.IntegerField(default=0)
	pic = models.URLField()
	ingredients = models.CharField(max_length=128) # prefer list of integers but might have to use string and parse!
	# allergies = models.IntegerField(default=0) ~ possible feature for end system
	# diet = models.IntegerField(default=0) ~ possible feature for end system
	slug = models.SlugField() # for post requests
	
	def save(self, *args, **kwargs):
	    self.slug = slugify(self.name)
	    super(Pizza, self).save(*args, **kwargs)
	
	def __unicode__(self):
	    return self.name


class Ingredient(models.Model):
	"""
	Ingredient
	- Stores name of ingredient and index of ingredients on pizza matrix with the amount with total counted in pizzas
	"""
	
	name = models.CharField(max_length=128)
	index = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	slug = models.SlugField()
	
	def save(self, *args, **kwargs):
	    self.slug = slugify(self.name)
	    super(Ingredient, self).save(*args, **kwargs)

	def __unicode__(self):
	    return self.name


class PairPreferance(models.Model):
	"""
	UserPreferance
	- Stores pair of pizza index, with 0 or 1 rating, used in comparsisons
	"""
	# Need link pair to user 
	user = models.IntegerField(default=0)
	# Index of pair
	index = models.IntegerField(default=0)
	# Value of pair
	value = models.IntegerField(default=2)
	# Date of pair made
	date = models.DateField(default=date.today())
	
	slug = models.SlugField()
	
	def save(self, *args, **kwargs):
	    self.slug = slugify(self.index)
	    super(PairPreferance, self).save(*args, **kwargs)
	
	def __unicode__(self):
		index = str(self.index)
		return index
