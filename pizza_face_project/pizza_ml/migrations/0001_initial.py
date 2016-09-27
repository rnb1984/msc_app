# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-27 18:01
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=228)),
                ('index', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=228)),
            ],
        ),
        migrations.CreateModel(
            name='PairPreferance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0)),
                ('index', models.IntegerField(default=0)),
                ('value', models.IntegerField(default=2)),
                ('date', models.DateField(default=datetime.date(2016, 9, 27))),
                ('time', models.IntegerField(default=0)),
                ('t_at', models.CharField(default=b'none', max_length=228)),
                ('pic', models.BooleanField(default=True)),
                ('browser', models.CharField(default=b'none', max_length=228)),
                ('scrn_h', models.IntegerField(default=0)),
                ('scrn_w', models.IntegerField(default=0)),
                ('scroll_x', models.IntegerField(default=0)),
                ('scroll_y', models.IntegerField(default=0)),
                ('exp_no', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=228)),
                ('index', models.IntegerField(default=0)),
                ('pic', models.URLField()),
                ('ingredients', models.CharField(max_length=228)),
                ('slug', models.SlugField(max_length=228)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_index', models.IntegerField(default=0)),
                ('dob', models.IntegerField(default=0)),
                ('gender', models.CharField(choices=[(b'U', b'Undisclosed'), (b'F', b'Female'), (b'M', b'Male')], default=b'U', max_length=1)),
                ('allergies', models.CharField(default=b'0', max_length=228)),
                ('diet', models.CharField(default=b'0', max_length=228)),
                ('occupation', models.IntegerField(default=0)),
                ('nationality', models.CharField(default=b'0', max_length=228)),
                ('permission', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
