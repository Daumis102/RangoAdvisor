# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-27 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor', '0004_location_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
