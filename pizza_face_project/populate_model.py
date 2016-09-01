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

from bba.models import Band, UserProfile, LikedBand, Gig, Venue, GigAttendance

from django.contrib.auth.models import User

API_KEY = "jwzmbEyCAIwD7HCy"

def populate():

    #added population script 


# Start execution here!
if __name__ == '__main__':
    print "Starting bandbuds model test script..."
    populate()