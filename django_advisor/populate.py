# file for populating the database with some data
import os
import django
from datetime import date
from django.core.files import File
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_advisor.settings')
django.setup()
from advisor.models import *


def populate(users):
    media_dir = os.path.join(os.getcwd(), 'media')
    locations = [
        {"name": "University of Glasgow",
         "city": "Glasgow",
         "coordinates": "55.8721,-4.2882",
         "visited_by": ",".join([str(users[0].id), str(users[3].id)])},
        {"name": "Taco Mazama",
         "city": "Glasgow",
         "coordinates": "55.8681753,-4.3278404",
         "visited_by": ",".join([str(users[1].id), str(users[2].id)])}
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
         "posted_by": users[0],
         "location_id": uofgloc},
        {"title": "Average food but good service",
         "publish_date": date.today(),
         "content": "The food was a bit bland and expensive, but the staff served me with a smile. They tried their best",
         "rating": 3,
         "posted_by": users[1],
         "location_id": tmloc},
        {"title": "Great",
         "publish_date": date.today(),
         "content": "I am definitely coming back here again",
         "rating": 4,
         "posted_by": users[2],
         "location_id": uofgloc},
        {"title": "Awful. Just awful",
         "publish_date": date.today(),
         "content": "Title says it all",
         "rating": 1,
         "posted_by": users[3],
         "location_id": tmloc}
    ]

    pictures = [
        {"upload_date": date.today(),
         "picture": File(open(media_dir+'/uofg0.jpg')),
         "location_id": uofgloc,
         "posted_by": users[0]},
        {"upload_date": date.today(),
         "picture": File(open(media_dir+'/uofg1.jpg')),
         "location_id": uofgloc,
         "posted_by": users[2]},
        {"upload_date": date.today(),
         "picture": File(open(media_dir+'/taco_mazama0.jpg')),
         "location_id": tmloc,
         "posted_by": users[1]},
        {"upload_date": date.today(),
         "picture": File(open(media_dir+'/taco_mazama1.jpg')),
         "location_id": tmloc,
         "posted_by": users[3]}
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
    user1 = User.objects.create_user(username="Mike", password="user1password", email="mike@gmail.com")
    user2 = User.objects.create_user(username="MaryJane", password="user2password", email="MaryJane@gmail.com")
    user3 = User.objects.create_user(username="Molly", password="user3password", email="Molly@gmail.com")
    user4 = User.objects.create_user(username="Robert", password="user4password", email="Robert@gmail.com")
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    for user in User.objects.all():
        if user.username in ["Mike", "MaryJane", "Molly", "Robert"]:  # ignore all users except the ones created just now
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
    print(users)
    populate(users)
