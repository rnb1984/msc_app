# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 12:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_ml', '0004_auto_20160902_1235'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
    ]
