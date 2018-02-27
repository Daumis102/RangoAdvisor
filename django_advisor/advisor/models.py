from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from utils.slugify import *


class Location(models.Model):
    name = models.CharField(max_length=50)  # the name of the location
    city = models.CharField(max_length=50)  # city where it is located
    coordinates = models.CharField(validators=[validate_comma_separated_integer_list], max_length=128)  # the latitude/longitude coordinates from maps api in comma separated string
    visited_by = models.CharField(validators=[validate_comma_separated_integer_list], max_length=128)  # list of the people who have visited this place
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name, slug_field_name='slug')
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Locations"

    def __str__(self):  # return the name of the location
        return self.name


class Comment(models.Model):
    publish_date = models.DateField(auto_now=True)  # the date that the comment was published
    content = models.CharField(max_length=300)  # the content of the comment
    location_id = models.PositiveIntegerField()  # foreign key pointing to the location which this comment belongs to
    rating = models.CharField(max_length=1)  # rating of 1 to 5
    posted_by = models.CharField(max_length=30)  # foreign key to user that posted this comment

    class Meta:
        verbose_name_plural = "Locations"

    def __str__(self):  # return the comment content when printed
        return self.content


class Picture(models.Model):
    upload_date = models.DateField(auto_now=True)  # the upload date of picture
    location_id = models.PositiveIntegerField()  # foreign key of the location that this picture is of
    uploaded_by = models.CharField(max_length=30)  # foreign key to the user that uploaded this picture
    picture = models.ImageField(upload_to='places_location', blank=True)  # the actual picture

    class Meta:
        verbose_name_plural = "Pictures"

    def __str__(self):  # unsure about this
        return self.picture
    

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)  # the user
    picture = models.ImageField(upload_to='profile_image', blank=True)  # picture of the user

    def __str__(self):  # return the username when printed
        return self.user.username

