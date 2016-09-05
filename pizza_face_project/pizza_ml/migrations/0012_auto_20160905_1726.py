# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-05 17:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_ml', '0011_remove_userprofile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(default='cheese'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=datetime.date(2016, 9, 5)),
        ),
    ]
