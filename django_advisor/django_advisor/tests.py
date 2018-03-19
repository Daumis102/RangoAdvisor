import os
from django.test import TestCase
from advisor.models import User, UserProfile

#TESTS DEFINITION
def test_pages_exist(page_names_list):
    for page in page_names_list:
        page += ".html"
        if os.path.exists("./templates/advisor/"):
            print("Existing: " + page)
        else:
            print ("Not existing: " + page)

def create_user():
    # Create a user
    user = User.objects.get_or_create(username="testuser", password="test1234")[0]
    user.set_password(user.password)
    user.save()
    user_profile.save()
    return user, user_profile


def test_population_script_changes(self):
    # Populate database
    populate_rango.populate()

    UniversityofGlasgow = Category.objects.get(name='University of Glasgow')
    self.assertEquals(UniversityofGlasgow.city, "Glasgow")
    self.assertEquals(UniversityofGlasgow.coordinates, "55.8721,-4.2882")

    TacoMazama = Category.objects.get(name='Taco Mazama')
    self.assertEquals(TacoMazama.city, "Glasgow")
    self.assertEquals(TacoMazama.coordinates, "55.8681753,-4.3278404")


class Chapter6ModelTests(TestCase):
    def test_category_contains_slug_field(self):
        #Create a new category
        new_category = add_location(name="Test Location")
        new_category.save()

        #Check slug was generated
        self.assertEquals(new_category.slug, "test-location")

        #Check there is only one category
        categories = Category.objects.all()
        self.assertEquals(len(categories), 1)

        #Check attributes were saved correctly
        categories[0].slug = new_category.slug

def test_base_template_exists(self):
    # Check base.html exists inside template folder
    return test_pages_exist("base")

#INITIALIZATION:
test_pages_exist(["about", "add_location", "base", "contacts", "index", "location_details"])
test_pages_exist(["/forms/login", "/forms/manual_address", "/forms/register", "/forms/write_review"])
create_user()
test_population_script_changes()
test_base_template_exists()
