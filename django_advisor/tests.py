import os


#TESTS DEFINITION
def test_pages_exist(page_names_list):
    for page in page_names_list:
        page += ".html"
        if os.path.exists("./templates/advisor/"):
            print("Existing: " + page)
        else:
            print ("Not existing: " + page)






#INITIONALIZATION:
test_pages_exist(["about", "add_location", "base", "contacts", "index", "location_details"])
test_pages_exist(["/forms/login", "/forms/manual_address", "/forms/register", "/forms/write_review"])

