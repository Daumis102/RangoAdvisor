from django.test import TestCase, Client
from .models import *

class ModelsTest(TestCase):
    def setUp(self):
        Location.objects.create(name="Caledonian UNi", city="Glasgow", coordinates="233, 233", slug="Caley")

    def test_get_lat(self):
        loc = Location.objects.get(city="Glasgow")
        self.assertEquals(loc.get_lat(), 233.0)

class ViewsTest(TestCase):
    def setUp(self):
        Location.objects.create(name="Caledonian UNi", city="Glasgow", coordinates="233, 233", slug="Caley")

    def test_index_page(self):
        c = Client()
        response = c.get("/advisor/index/")
        self.assertContains(response, "Caledonian")
