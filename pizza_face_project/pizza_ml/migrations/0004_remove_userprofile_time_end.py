# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-23 21:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_ml', '0003_auto_20160923_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='time_end',
        ),
    ]