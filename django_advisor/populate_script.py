# file for populating the database with some data
import os
import django
from datetime import date
from tqdm import tqdm
from django.core.files import File
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_advisor.settings')
django.setup()
from advisor.models import *


# helper method for title casing and taking care of apostrophes
def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(), s)


def populate(users):
    init_image_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'django_advisor', 'media', 'initial_population'))

    bean_visited = [users[0].id]
    highlands_visited = [users[0].id, users[1].id, users[2].id]
    nyhavn_visited = [users[0].id]
    stonehenge_visited = [users[3].id]
    yucatan_visited = [users[1].id]

    locations = [
        {
            "name": titlecase("Cloud Gate"),
            "city": titlecase("Chicago"),
            "coordinates": "41.8826,-87.6254",
            "visited_by": ",".join(map(str, bean_visited))
        },
        {
            "name": titlecase("Loch Lomond"),
            "city": titlecase("Balloch"),
            "coordinates": "56.1366,-4.7398",
            "visited_by": ",".join(map(str, highlands_visited))
        },
        {
            "name": titlecase("Nyhavn"),
            "city": titlecase("Copenhagen"),
            "coordinates": "55.6797,12.5864",
            "visited_by": ",".join(map(str, nyhavn_visited))
        },
        {
            "name": titlecase("Stonehenge"),
            "city": titlecase("Salisbury"),
            "coordinates": "51.1788,-1.8284",
            "visited_by": ",".join(map(str, stonehenge_visited))
        },
        {
            "name": titlecase("Chichen Itza"),
            "city": titlecase("Yucatan"),
            "coordinates": "20.6842,-88.5699",
            "visited_by": ",".join(map(str, yucatan_visited))
        }
    ]

    # first add locations
    print("Adding locations...")
    for loc in tqdm(locations):
        add_location(loc.get("name"), loc.get("city"), loc.get("coordinates"), loc.get("visited_by"))
    print("Locations added!")

    bean_loc = Location.objects.get(name="Cloud Gate")
    highlands_loc = Location.objects.get(name="Loch Lomond")
    nyhavn_loc = Location.objects.get(name="Nyhavn")
    stonehenge_loc = Location.objects.get(name="Stonehenge")
    yucatan_loc = Location.objects.get(name="Chichen Itza")

    reviews = [
        {
            "title": titlecase("What a gorgeous view"),
            "publish_date": date.today(),
            "content": "The Cloud Gat, or Bean as the Chicagoans call it, is truly a sight to behold. Quite an impressive piece of engineering.",
            "rating": 5,
            "posted_by": UserProfile.objects.get(user=users[0]),
            "location_id": bean_loc
        },
        {
            "title": titlecase("Good place"),
            "publish_date": date.today(),
            "content": "Wow what an incredible place, I am definitely visiting again",
            "rating": 5,
            "posted_by": UserProfile.objects.get(user=users[0]),
            "location_id": highlands_loc
        },
        {
            "title": titlecase("Views are phenomenal"),
            "publish_date": date.today(),
            "content": "You have to stand at the very top to understand",
            "rating": 4,
            "posted_by": UserProfile.objects.get(user=users[1]),
            "location_id": highlands_loc
        },
        {
            "title": titlecase("Quite cold"),
            "publish_date": date.today(),
            "content": "It was very cold and rainy when I went, the weather app predicted it to be sunny and clear. Dissapointed",
            "rating": 2,
            "posted_by": UserProfile.objects.get(user=users[2]),
            "location_id": highlands_loc
        },
        {
            "title": titlecase("Good place"),
            "publish_date": date.today(),
            "content": "Wow what an incredible place, I am definitely visiting again",
            "rating": 5,
            "posted_by": UserProfile.objects.get(user=users[0]),
            "location_id": nyhavn_loc
        },
        {
            "title": titlecase("A great, big, beautiful rock"),
            "publish_date": date.today(),
            "content": "The pioneers used to ride these babies for miles",
            "rating": 5,
            "posted_by": UserProfile.objects.get(user=users[3]),
            "location_id": stonehenge_loc
        },
        {
            "title": titlecase("What a gorgeous view"),
            "publish_date": date.today(),
            "content": "Lovely to see such a work of history",
            "rating": 5,
            "posted_by": UserProfile.objects.get(user=users[1]),
            "location_id": yucatan_loc
        }
    ]

    # oh boy. could have looped thru each directory and stored in a list but that's a feature not a requirement
    bean_i1 = open(os.path.join(init_image_dir, 'bean', 'bean1r.jpg'), 'rb')
    highlands_i1 = open(os.path.join(init_image_dir, 'highlands', 'gh1r.jpg'), 'rb')
    highlands_i2 = open(os.path.join(init_image_dir, 'highlands', 'gh2r.jpg'), 'rb')
    highlands_i3 = open(os.path.join(init_image_dir, 'highlands', 'gh3r.jpg'), 'rb')
    nyhavn_i1 = open(os.path.join(init_image_dir, 'nyhavn', 'cph1r.jpg'), 'rb')
    nyhavn_i2 = open(os.path.join(init_image_dir, 'nyhavn', 'cph2r.jpg'), 'rb')
    nyhavn_i3 = open(os.path.join(init_image_dir, 'nyhavn', 'cph3r.jpg'), 'rb')
    stonehenge_i1 = open(os.path.join(init_image_dir, 'stonehenge', 'sth1r.jpg'), 'rb')
    stonehenge_i2 = open(os.path.join(init_image_dir, 'stonehenge', 'sth2r.jpg'), 'rb')
    yucatan_i1 = open(os.path.join(init_image_dir, 'yucatan', 'yucatan1r.jpg'), 'rb')
    yucatan_i2 = open(os.path.join(init_image_dir, 'yucatan', 'yucatan2r.jpg'), 'rb')

    pictures = [
        {
            "upload_date": date.today(),
            "picture": File(bean_i1, 'rb'),
            "location_id": bean_loc,
            "uploaded_by": UserProfile.objects.get(user=users[0])
        },
        {
            "upload_date": date.today(),
            "picture": File(highlands_i1, 'rb'),
            "location_id": highlands_loc,
            "uploaded_by": UserProfile.objects.get(user=users[0])
        },
        {
            "upload_date": date.today(),
            "picture": File(highlands_i2, 'rb'),
            "location_id": highlands_loc,
            "uploaded_by": UserProfile.objects.get(user=users[1])
        },
        {
            "upload_date": date.today(),
            "picture": File(highlands_i3, 'rb'),
            "location_id": highlands_loc,
            "uploaded_by": UserProfile.objects.get(user=users[2])
        },
        {
            "upload_date": date.today(),
            "picture": File(nyhavn_i1, 'rb'),
            "location_id": nyhavn_loc,
            "uploaded_by": UserProfile.objects.get(user=users[0])
        },
        {
            "upload_date": date.today(),
            "picture": File(nyhavn_i2, 'rb'),
            "location_id": nyhavn_loc,
            "uploaded_by": UserProfile.objects.get(user=users[0])
        },
        {
            "upload_date": date.today(),
            "picture": File(nyhavn_i3, 'rb'),
            "location_id": nyhavn_loc,
            "uploaded_by": UserProfile.objects.get(user=users[0])
        },
        {
            "upload_date": date.today(),
            "picture": File(stonehenge_i1, 'rb'),
            "location_id": stonehenge_loc,
            "uploaded_by": UserProfile.objects.get(user=users[3])
        },
        {
            "upload_date": date.today(),
            "picture": File(stonehenge_i2, 'rb'),
            "location_id": stonehenge_loc,
            "uploaded_by": UserProfile.objects.get(user=users[3])
        },
        {
            "upload_date": date.today(),
            "picture": File(yucatan_i1, 'rb'),
            "location_id": yucatan_loc,
            "uploaded_by": UserProfile.objects.get(user=users[1])
        },
        {
            "upload_date": date.today(),
            "picture": File(yucatan_i2, 'rb'),
            "location_id": yucatan_loc,
            "uploaded_by": UserProfile.objects.get(user=users[1])
        }
    ]

    # then add reviews
    print("Adding reviews...")
    for review in tqdm(reviews):
        add_review(title=review.get("title"), publish_date=review.get("publish_date"), content=review.get("content"),
                   rating=review.get("rating"), posted_by=review.get("posted_by"),
                   location_id=review.get("location_id"))
    print("Reviews added!")
    # finally add the pictures
    print("Adding pictures...")
    for picture in tqdm(pictures):
        add_picture(upload_date=picture.get("upload_date"), picture=picture.get("picture"),
                    uploaded_by=picture.get("uploaded_by"), location_id=picture.get("location_id"))
    print("Pictures added!")


def add_some_users():
    init_image_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'django_advisor', 'static', 'images'))
    # to add some users to the database which will help in populating everything else
    new_users = []
    user1 = User.objects.create_user(username="anguel", password="anguel", email="anguel@gmail.com")
    user2 = User.objects.create_user(username="daumantas", password="daumantas", email="daumantas@gmail.com")
    user3 = User.objects.create_user(username="louis", password="louis", email="louis@gmail.com")
    user4 = User.objects.create_user(username="soma", password="soma", email="soma@gmail.com")
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    user1profile = UserProfile.objects.create(user=user1, avatar=File(open(os.path.join(init_image_dir, 'default_avatar.png'), 'rb'), 'rb'))
    user2profile = UserProfile.objects.create(user=user2, avatar=File(open(os.path.join(init_image_dir, 'default_avatar.png'), 'rb'), 'rb'))
    user3profile = UserProfile.objects.create(user=user3, avatar=File(open(os.path.join(init_image_dir, 'default_avatar.png'), 'rb'), 'rb'))
    user4profile = UserProfile.objects.create(user=user4, avatar=File(open(os.path.join(init_image_dir, 'default_avatar.png'), 'rb'), 'rb'))
    user1profile.save()
    user2profile.save()
    user3profile.save()
    user4profile.save()
    print("Adding sample users...")
    for user in tqdm(User.objects.all()):
        if user.username in ["anguel", "daumantas", "louis",
                             "soma"]:  # ignore all users except the ones created just now. this is done in case there are already other users in db
            new_users.append(user)
    print("Users added!")
    return new_users


def add_review(title, publish_date, content, rating, location_id, posted_by):
    review = Review.objects.get_or_create(title=title, publish_date=publish_date, content=content, rating=rating,
                                          location_id=location_id, posted_by=posted_by)[0]
    review.save()
    return review


def add_location(name, city, coordinates, visited_by):
    location = Location.objects.get_or_create(name=name, city=city, coordinates=coordinates, visited_by=visited_by)[0]
    location.save()
    return location


def add_picture(upload_date, picture, uploaded_by, location_id):
    picture = Picture.objects.get_or_create(upload_date=upload_date, picture=picture, uploaded_by=uploaded_by,
                                            location_id=location_id)[0]
    picture.save()
    return picture


if __name__ == '__main__':
    print("Starting population script...")
    u = add_some_users()
    populate(u)
    print("Population script done!")
