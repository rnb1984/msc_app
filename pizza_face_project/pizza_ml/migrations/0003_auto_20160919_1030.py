# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-19 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_ml', '0002_auto_20160919_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='exp_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='nationality',
            field=models.IntegerField(default=0),
        ),
    ]
