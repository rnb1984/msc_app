# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-26 20:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_ml', '0004_remove_userprofile_time_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=228),
        ),
        migrations.AlterField(
            model_name='pairpreferance',
            name='date',
            field=models.DateField(default=datetime.date(2016, 9, 26)),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='ingredients',
            field=models.CharField(max_length=228),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='name',
            field=models.CharField(max_length=228),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='allergies',
            field=models.CharField(default=b'0', max_length=228),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='diet',
            field=models.CharField(default=b'0', max_length=228),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nationality',
            field=models.CharField(default=b'0', max_length=228),
        ),
    ]