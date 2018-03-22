import re
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User


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

    def get_picture(self):
        try:
            picture = Picture.objects.filter(location_id=self.id)[0]
            print(picture)
        except:
            picture = None
        return picture

    def get_rating(self):
        reviews = Review.objects.filter(location_id=self.id)
        if len(reviews) > 0:
            rating_sum = 0
            for review in reviews:
                rating_sum += int(review.rating)
            return round(rating_sum/len(reviews), 1)
        else:
            return None

    def num_reviews(self):
        review = Review.objects.filter(location_id=self.id)
        return len(review)
    
    def visited_by_list(self):
        return self.visited_by.split(',')

    def num_visited_by(self):
        return len(self.visited_by.split(','))
        

class Review(models.Model):
    title = models.CharField(max_length=100, default="")
    publish_date = models.DateField(auto_now=True)  # the date that the comment was published
    content = models.CharField(max_length=300)  # the content of the comment
    rating = models.IntegerField()  # rating of 1 to 5
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)  # actual foreign key
    posted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # actual foreign key

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):  # return the comment content when printed
        return self.content


class Picture(models.Model):
    upload_date = models.DateField(auto_now=True)  # the upload date of picture
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)  # actual foreign key
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # actual foreign key
    picture = models.ImageField(upload_to='places_location', blank=True, max_length=1000)  # the actual picture

    class Meta:
        verbose_name_plural = "Pictures"

    def __str__(self):
        return str(self.location_id.name) + " " + str(self.id)


# Custom slugiy for unique slugs
def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
