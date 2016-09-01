from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.core.validators import validate_email
from django.template.defaultfilters import slugify
from datetime import date

"""
!!! TO DO !!!
# Write all models
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
    dob = models.DateField(default=date.today())
    gender = models.CharField(default="U", max_length=1, choices=GENDER_CHOICES)
    allergies = models.IntegerField(default=0)
    diet = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
         self.slug = slugify(self.user)
         super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


# DEFINE MODEL !!!
class Pizza(models.Model):
	"""
	Pizza
	- Stores name of pizza, pic of pizza, index pizza is on matrix of pizza and a feature vecture of ingredients
	"""

	name = models.CharField(max_length=128) # maybe bigger!!
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

# DEFINE MODEL !!!
class Ingredients(models.Model):
	"""
	Ingredients
	- Stores name of ingredients and index of ingredients on pizza matrix
	"""
	name = models.CharField(max_length=128) # maybe bigger!!
	index = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
         self.slug = slugify(self.name)
         super(Ingredients, self).save(*args, **kwargs)

	def __unicode__(self):
	    return self.name


# DEFINE MODEL !!!	
class UserPreferance(models.Model):
	"""
	UserPreferance
	- Stores pizza pair index, with 0 or 1 rating, used in comparsisons
	- Stores latest prediction as pizza index integer
	- Stores boolean for if prediction was true or false
	"""

	# Pair index dictionary with values of evaluated pairs
	pairs = models.CharField(max_length=128)
	# Current prediction = int
	predict = models.IntegerField(default=0)
	# Prediction correct = boolean
	correct = models.BooleanField(default=False)
	
	def __unicode__(self):
	    return self.predict