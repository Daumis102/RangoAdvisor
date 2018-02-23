from django.db import models
from django.contrib.auth.models import User

# TODO PageModel, ReviewModel

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # additional attributes
    
    picture = models.ImageField(upload_to='profile_image', blank=True)
    # TODO add Reviews
    # TODO add Pages visited

    def __str__(self):
        return self.user.username
