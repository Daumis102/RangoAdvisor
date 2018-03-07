from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from utils.slugify import *


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)  # the user
    avatar = models.ImageField(upload_to='profile_image', blank=True, null=True)  # picture of the user

    def __str__(self):  # return the username when printed
        return self.user.username


class Location(models.Model):
    name = models.CharField(max_length=50)  # the name of the location
    city = models.CharField(max_length=50)  # city where it is located
    coordinates = models.CharField(max_length=128)  # the latitude/longitude coordinates from maps api in comma separated string
    visited_by = models.CharField(validators=[validate_comma_separated_integer_list], max_length=128, blank=True)  # list of the people who have visited this place
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name, slug_field_name='slug')
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Locations"

    def __str__(self):  # return the name of the location
        return self.name
    
    def get_lat(self):
        return float(self.coordinates.split(',')[0])
    
    def get_lng(self):
        return float(self.coordinates.split(',')[1])


class Review(models.Model):
    title = models.CharField(max_length=100, default="")
    publish_date = models.DateField(auto_now=True)  # the date that the comment was published
    content = models.CharField(max_length=300)  # the content of the comment
    rating = models.CharField(max_length=1)  # rating of 1 to 5
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)  # actual foreign key
    # location_id = models.PositiveIntegerField()  # foreign key pointing to the location which this comment belongs to
    posted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # actual foreign key
    # posted_by = models.CharField(max_length=30)  # foreign key to user that posted this comment

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):  # return the comment content when printed
        return self.content


class Picture(models.Model):
    upload_date = models.DateField(auto_now=True)  # the upload date of picture
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)  # actual foreign key
    # location_id = models.PositiveIntegerField()  # foreign key of the location that this picture is of
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # actual foreign key
    # uploaded_by = models.CharField(max_length=30)  # foreign key to the user that uploaded this picture
    picture = models.ImageField(upload_to='places_location', blank=True, max_length=1000)  # the actual picture

    class Meta:
        verbose_name_plural = "Pictures"

    def __str__(self):
        return str(self.location_id.name) + " " + str(self.id)
