# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-04 18:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_ml', '0010_auto_20160904_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='slug',
        ),
    ]
