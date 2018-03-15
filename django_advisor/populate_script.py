# file for populating the database with some data
import os
import django
from datetime import date
from django.core.files import File
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_advisor.settings')
django.setup()
from advisor.models import *


def populate(users):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    init_image_dir = os.path.normpath(os.path.join(BASE_DIR, 'django_advisor', 'media', 'initial_population'))

    uofgvisited = [users[0].id, users[3].id]
    tmvisited = [users[1].id, users[2].id]

    locations = [
        {"name": "University of Glasgow",
         "city": "Glasgow",
         "coordinates": "55.8721,-4.2882",
         "visited_by": ",".join(map(str, uofgvisited))},
        {"name": "Taco Mazama",
         "city": "Glasgow",
         "coordinates": "55.8681753,-4.3278404",
         "visited_by": ",".join(map(str, tmvisited))}
    ]

    # first add locations
    for loc in locations:
        add_location(loc.get("name"), loc.get("city"), loc.get("coordinates"), loc.get("visited_by"))

    uofgloc = Location.objects.get(name="University of Glasgow")
    tmloc = Location.objects.get(name="Taco Mazama")

    reviews = [
        {"title": "Good place",
         "publish_date": date.today(),
         "content": "Wow what an incredible place, I am definitely visiting again",
         "rating": 5,
         "posted_by": UserProfile.objects.get(user=users[0]),
         "location_id": uofgloc},
        {"title": "Average food but good service",
         "publish_date": date.today(),
         "content": "The food was a bit bland and expensive, but the staff served me with a smile. They tried their best",
         "rating": 3,
         "posted_by": UserProfile.objects.get(user=users[1]),
         "location_id": tmloc},
        {"title": "Great",
         "publish_date": date.today(),
         "content": "I am definitely coming back here again",
         "rating": 4,
         "posted_by": UserProfile.objects.get(user=users[2]),
         "location_id": uofgloc},
        {"title": "Awful. Just awful",
         "publish_date": date.today(),
         "content": "Title says it all",
         "rating": 1,
         "posted_by": UserProfile.objects.get(user=users[3]),
         "location_id": tmloc}
    ]

    uofgi0 = open(os.path.join(init_image_dir, 'uofg0.jpg'), 'rb')
    uofgi1 = open(os.path.join(init_image_dir, 'uofg1.jpg'), 'rb')
    tmi0 = open(os.path.join(init_image_dir, 'taco_mazama0.jpg'), 'rb')
    tmi1 = open(os.path.join(init_image_dir, 'taco_mazama1.jpg'), 'rb')

    pictures = [
        {"upload_date": date.today(),
         "picture": File(uofgi0, 'rb'),
         "location_id": uofgloc,
         "uploaded_by": UserProfile.objects.get(user=users[0])},
        {"upload_date": date.today(),
         "picture": File(uofgi1, 'rb'),
         "location_id": uofgloc,
         "uploaded_by": UserProfile.objects.get(user=users[2])},
        {"upload_date": date.today(),
         "picture": File(tmi0, 'rb'),
         "location_id": tmloc,
         "uploaded_by": UserProfile.objects.get(user=users[1])},
        {"upload_date": date.today(),
         "picture": File(tmi1, 'rb'),
         "location_id": tmloc,
         "uploaded_by": UserProfile.objects.get(user=users[3])}
    ]

    # then add reviews
    for review in reviews:
        add_review(title=review.get("title"), publish_date=review.get("publish_date"), content=review.get("content"), rating=review.get("rating"), posted_by=review.get("posted_by"), location_id=review.get("location_id"))

    # finally add the pictures
    for picture in pictures:
        add_picture(upload_date=picture.get("upload_date"), picture=picture.get("picture"), uploaded_by=picture.get("uploaded_by"), location_id=picture.get("location_id"))


def add_some_users():
    # to add some users to the database which will help in populating everything else
    u = []
    user1 = User.objects.create_user(username="Mike", password="mikepassword", email="mike@gmail.com")
    user2 = User.objects.create_user(username="Mary", password="marypassword", email="mary@gmail.com")
    user3 = User.objects.create_user(username="Molly", password="mollypassword", email="molly@gmail.com")
    user4 = User.objects.create_user(username="Robert", password="robertpassword", email="robert@gmail.com")
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    user1profile = UserProfile.objects.create(user=user1, avatar=None)
    user2profile = UserProfile.objects.create(user=user2, avatar=None)
    user3profile = UserProfile.objects.create(user=user3, avatar=None)
    user4profile = UserProfile.objects.create(user=user4, avatar=None)
    user1profile.save()
    user2profile.save()
    user3profile.save()
    user4profile.save()
    for user in User.objects.all():
        if user.username in ["Mike", "Mary", "Molly", "Robert"]:  # ignore all users except the ones created just now
            u.append(user)
    return u


def add_review(title, publish_date, content, rating, location_id, posted_by):
    review = Review.objects.get_or_create(title=title, publish_date=publish_date, content=content, rating=rating, location_id=location_id, posted_by=posted_by)[0]
    review.save()
    return review


def add_location(name, city, coordinates, visited_by):
    location = Location.objects.get_or_create(name=name, city=city, coordinates=coordinates, visited_by=visited_by)[0]
    location.save()
    return location


def add_picture(upload_date, picture, uploaded_by, location_id):
    picture = Picture.objects.get_or_create(upload_date=upload_date, picture=picture, uploaded_by=uploaded_by, location_id=location_id)[0]
    picture.save()
    return picture


if __name__ == '__main__':
    users = add_some_users()
    populate(users)
