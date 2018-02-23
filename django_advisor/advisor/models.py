from django.db import models
from django.contrib.auth.models import User

# TODO  Location,

class Comment(model.Model):
    publish_date = models.DateField(auto_now=True)
    content = models.CharField(max_length=300)
    location_id = models.PositiveIntegerField()
    rating = models.CharField(max_length=1)
    posted_by = models.CharField(max_length=30)

class Picture(model.Model):
    upload_date = models.DateField(auto_now=True)
    location_id = models.PositiveIntegerField()
    uploaded_by = models.CharField(max_length=30)
    

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # additional attributes
    
    picture = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username
