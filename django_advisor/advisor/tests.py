from datetime import date
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import SESSION_KEY
from advisor.views import *
from .models import *


# helper methods for the setUp functions to reduce the same boilerplate
def get_init_dir():
    return os.path.normpath(
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ''))


def get_user_info():
    return {'username': 'anguel', 'password': 'anguel', 'email': 'anguel@gmail.com'}


def get_loc_info(i):
    return {'name': 'Caledonian Uni', 'city': 'Glasgow', 'coordinates': '233,233',
            'visited_by': ','.join(map(str, [i]))}


def get_rev_info(u, l):
    return {'title': 'What a gorgeous view', 'publish_date': date.today(),
            'content': 'The Cloud Gat, or Bean as the Chicagoans call it, is truly a sight to behold. Quite an impressive piece of engineering.',
            'rating': 5, 'posted_by': UserProfile.objects.get(user=u), 'location_id': l}


def get_prof_info(u):
    return {'user': u,
            'avatar': File(open(os.path.join(get_init_dir(), 'static', 'images', 'default_avatar.png'), 'rb'), 'rb')}


def get_pic_info(u, l):
    return {'upload_date': date.today(), 'picture': File(
        open(os.path.join(get_init_dir(), 'media', 'initial_population', 'bean', 'bean1.jpg'), 'rb'), 'rb'),
            'location_id': l, 'uploaded_by': UserProfile.objects.get(user=u)}


class LocationTests(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))
        self.loc = Location.objects.create(**get_loc_info(self.user.id))
        self.rev = Review.objects.create(**get_rev_info(self.user, self.loc))
        self.pic = Picture.objects.create(**get_pic_info(self.user, self.loc))

    def test_get_lat(self):
        self.assertEquals(self.loc.get_lat(), 233)

    def test_get_lng(self):
        self.assertEqual(self.loc.get_lng(), 233)

    def test_to_str(self):
        self.assertEqual(str(self.loc), self.loc.name)

    def test_get_picture(self):
        self.assertEqual(self.loc.get_picture(),
                         self.pic)  # this works cause the picture is mapped to this location in the setup

    def test_get_rating(self):
        self.assertEqual(self.loc.get_rating(), 5)

    def test_num_reviews(self):
        self.assertEqual(self.loc.num_reviews(), 1)

    def test_num_visited(self):
        self.assertEqual(self.loc.num_visited_by(), 1)

    def test_visited_by(self):
        self.assertIn(str(self.user.id), self.loc.visited_by_list())


class UserTests(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))

    def test_to_str(self):
        self.assertEqual(str(self.profile), self.user.username)


class ReviewTests(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))
        self.loc = Location.objects.create(**get_loc_info(self.user.id))
        self.rev = Review.objects.create(**get_rev_info(self.user, self.loc))

    def test_to_str(self):
        self.assertEqual(str(self.loc), self.loc.name)


class PictureTests(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))
        self.loc = Location.objects.create(**get_loc_info(self.user.id))
        self.pic = Picture.objects.create(**get_pic_info(self.user, self.loc))

    def test_to_str(self):
        self.assertEqual(str(self.pic), (self.pic.location_id.name + " " + str(self.pic.id)))


class ViewsTest(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))
        self.loc = Location.objects.create(**get_loc_info(self.user.id))
        self.rev = Review.objects.create(**get_rev_info(self.user, self.loc))
        self.pic = Picture.objects.create(**get_pic_info(self.user, self.loc))
        self.client = Client()
        self.factory = RequestFactory()

    def test_index_page(self):
        resp = self.client.get('/advisor/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Caledonian Uni')
        # test both routes
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Caledonian Uni')

    def test_contacts_page(self):
        resp = self.client.get('/advisor/contacts/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Daumantas')

    def test_about_page(self):
        resp = self.client.get('/advisor/contacts/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'DjangoAdvisor')

    def test_location_page(self):
        loc = Location.objects.get(name='Caledonian Uni', city='Glasgow', coordinates='233,233')
        resp = self.client.get('/advisor/location/{}/'.format(loc.slug))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Caledonian Uni')

    def test_add_location_page_logged_in(self):
        req = self.factory.get('/advisor/add_location/')
        req.user = self.user
        req.profile = self.profile
        resp = add_location(req)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Fill out the details to add a new location')  # logged in and can add details

    def test_add_location_page_logged_out(self):
        resp = self.client.get('/advisor/add_location/')
        self.assertEqual(resp.status_code, 302)  # redirect if anon wants to add location
        self.assertIn(resp.url, '/accounts/login/?next=/advisor/add_location/')

    def test_profile_page_logged_in(self):
        req = self.factory.get('/advisor/profile')
        req.user = self.user
        req.profile = self.profile
        resp = profile(req)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp,
                            'Username: '.format(self.user.username))  # show profile when logged in. check for username

    def test_profile_page_logged_out(self):
        resp = self.client.get('/advisor/profile')
        self.assertEqual(resp.status_code, 301)  # redirect if logged out
        self.assertIn(resp.url, '/advisor/profile/')

    def test_log_in(self):
        resp = self.client.post('/advisor/login/', {'username': ['anguel'], 'password': ['anguel']})
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='anguel', password='anguel')
        self.assertTrue(SESSION_KEY in self.client.session)  # now logged in

    def test_log_out(self):
        self.client.login(username='anguel', password='anguel')
        self.assertTrue(SESSION_KEY in self.client.session)
        resp = self.client.get('/advisor/logout/')
        self.assertEqual(resp.status_code, 302)  # redirect if they try to go to logout when not logged in
        self.assertIn(resp.url, '/advisor/index/')

    def test_loc_pic_upload(self):
        req = self.factory.post('/advisor/photo/upload/', {'photo': File(
            open(os.path.join(self.init_dir, 'media', 'initial_population', 'bean', 'bean1.jpg'), 'rb'), 'rb'),
            'location': '{}'.format(self.loc.slug)})
        req.user = self.user
        req.profile = self.profile
        self.assertEqual(len(Picture.objects.all()), 1)  # originally has 1 pic
        resp = upload_location_photo(req)
        self.assertEqual(len(Picture.objects.all()), 2)  # now has 2 pics
        self.assertEqual(resp.status_code, 200)

    def test_del_acc(self):
        self.client.login(username='anguel', password='anguel')  # show there is user currently in db
        self.assertTrue(SESSION_KEY in self.client.session)
        req = self.factory.post('/advisor/profile/deleteaccount/')
        req.user = self.user
        req.profile = self.profile
        resp = delete_account(req)
        self.client.logout()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)  # no logged in user
        self.assertEqual(len(User.objects.all()), 0)  # show no users in db

    def test_toggle_visited(self):
        req = self.factory.post('/advisor/location/toggle-visited', {'location_id': self.loc.id})
        req.user = self.user
        req.profile = self.profile
        resp = toggle_visited(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.loc.visited_by_list()), 1)


class TestSlugify(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))
        self.loc = Location.objects.create(**get_loc_info(self.user.id))
        self.rev = Review.objects.create(**get_rev_info(self.user, self.loc))
        self.pic = Picture.objects.create(**get_pic_info(self.user, self.loc))
        self.client = Client()
        self.factory = RequestFactory()

    def test_two_same_loc(self):
        new_loc = Location.objects.create(name='Caledonian Uni', city='Glasgow', coordinates='235,235',
                                          visited_by=','.join(map(str, [self.user.id])))
        new_loc.save()
        self.assertNotEquals(self.loc.slug, new_loc.slug)


class FormsTest(TestCase):
    def setUp(self):
        self.init_dir = get_init_dir()
        self.user = User.objects.create_user(**get_user_info())
        self.profile = UserProfile.objects.create(**get_prof_info(self.user))
        self.loc = Location.objects.create(**get_loc_info(self.user.id))
        self.rev = Review.objects.create(**get_rev_info(self.user, self.loc))
        self.pic = Picture.objects.create(**get_pic_info(self.user, self.loc))
        self.client = Client()
        self.factory = RequestFactory()

    def test_register_form(self):
        self.assertEqual(len(User.objects.all()), 1)  # first show there is only 1 user, created during setup
        resp = self.client.post('/advisor/register/',
                                {'username': ['testUser'], 'password': ['test'], 'passwordConfirm': ['test'],
                                 'currentUrl': ['/advisor/index/']})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(User.objects.all()), 2)  # now show there is a new one
        self.assertJSONEqual(str(resp.content, encoding='utf8'),
                             {'statusCode': 0, 'currentUrl': '/advisor/index/'})

    def test_signin_form(self):
        resp = self.client.post('/advisor/login/', {'username': ['anguel'], 'password': ['anguel']})
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='anguel', password='anguel')
        self.assertTrue(SESSION_KEY in self.client.session)

    def test_add_location_form(self):
        req = self.factory.post('/advisor/add_location/',
                                {'location_name': ['Loch Lomond'], 'city': ['Balloch'], 'coords': ['56.1366,-4.7398'],
                                 'review-title': ['Superb'], 'location_image': [File(
                                    open(
                                        os.path.join(self.init_dir, 'media', 'initial_population', 'bean', 'bean1.jpg'),
                                        'rb'), 'rb')], 'input-rating': 4, 'review-content': 'Very nice place'})
        req.user = self.user
        req.profile = self.profile
        self.assertEqual(len(Location.objects.all()), 1)  # show before adding new place that there is only one in db
        resp = add_location(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Location.objects.all()), 2)  # now there is the new place

    def test_changepassword_form(self):
        req = self.factory.post('/advisor/changepw/',
                                {'changePWPassword': ['newPassword']})
        req.user = self.user
        req.profile = self.profile
        resp = change_pw(req)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf8'),
                             {'statusCode': 0})

    def test_changeavatar_pseudo_form(self):
        req = self.factory.post('/advisor/change_pp/',
                                {'newAvatar': [File(
                                    open(
                                        os.path.join(self.init_dir, 'media', 'initial_population', 'bean', 'bean1.jpg'),
                                        'rb'), 'rb')]})
        original_avatar = self.profile.avatar.chunks(2)  # first 2 chunks of original avatar
        req.user = self.user
        req.profile = self.profile
        resp = change_pp(req)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(str(resp.content, encoding='utf8'),
                             {'statusCode': 0})
        self.assertNotEqual(self.profile.avatar.chunks(2),
                            original_avatar)  # first 2 chunks of new avatar should not be equal to the first 2 of the original

    def test_write_review_form(self):
        req = self.factory.post('/advisor/write_review/',
                                {'reviewTitle': 'Alright', 'input-rating': 3, 'reviewContent': 'Place is ok',
                                 'slug': self.loc.slug})
        req.user = self.user
        req.profile = self.profile
        self.assertEqual(len(Review.objects.all()), 1)  # originally start with 1 review
        resp = write_review(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Review.objects.all()), 2)  # new review added so now 2
