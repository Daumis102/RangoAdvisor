# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-25 17:05
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('coordinates', models.CharField(max_length=128)),
                ('visited_by', models.CharField(blank=True, max_length=128, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_date', models.DateField(auto_now=True)),
                ('picture', models.ImageField(blank=True, max_length=1000, upload_to='places_location')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisor.Location')),
            ],
            options={
                'verbose_name_plural': 'Pictures',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('publish_date', models.DateField(auto_now=True)),
                ('content', models.CharField(max_length=300)),
                ('rating', models.IntegerField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisor.Location')),
            ],
            options={
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profile_image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisor.UserProfile'),
        ),
        migrations.AddField(
            model_name='picture',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advisor.UserProfile'),
        ),
    ]
