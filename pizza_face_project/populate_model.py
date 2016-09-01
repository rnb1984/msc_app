#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BandBuds.settings')

import json
import urllib
import urllib2
from datetime import date
from django.core.validators import validate_email
import django
django.setup()
from django.core.validators import validate_email

from pizza_ml.models import Pizza, User, Ingredients

from django.contrib.auth.models import User


def populate():
    #added population script
    


# Start execution here!
if __name__ == '__main__':
    print "Starting pizza face model test script..."
    populate()