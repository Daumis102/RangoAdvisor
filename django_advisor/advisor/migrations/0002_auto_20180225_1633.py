# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-25 16:33
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('advisor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.PositiveIntegerField()),
                ('coordinates', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('visited_by', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
            ],
            options={
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': 'Locations'},
        ),
        migrations.AlterModelOptions(
            name='picture',
            options={'verbose_name_plural': 'Pictures'},
        ),
    ]