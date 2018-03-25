from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from advisor.models import *
import datetime
import os


def about(request):
    # show the about page
    return render(request, 'advisor/about.html', context={})


def contacts(request):
    # show the contacts page
    return render(request, 'advisor/contacts.html', context={})


def index(request):
    # show the index page with all the locations
    context_dict = {}
    locations_list = Location.objects.order_by('-name')  # get all the locations and order them by name
    visited_places = []
    user = str(request.user.id)
    for location in locations_list: 
        if user in location.visited_by_list():
            visited_places.append(location)  # get all the locations visited by the current user
    context_dict['locations'] = locations_list
    context_dict['visited_places'] = visited_places
    return render(request, 'advisor/index.html', context_dict)


@login_required
def add_location(request):
    # accept the form data and add that location to the database
    context_dict = {}
    if request.method == 'POST' and request.is_ajax():  # will just post back to the same url but with data
        # get all the fields from the post request
        coordinates = request.POST.get('coords')
        name = titlecase(request.POST.get('location_name'))
        image = request.FILES.get('location_image')
        rating = request.POST.get('input-rating')  # not used yet
        title = titlecase(request.POST.get('review-title'))
        content = request.POST.get('review-content')
        city = titlecase(request.POST.get('city'))
        current_user = request.user  # by this point the user must be logged in
        # if location exists, then do not recreate it
        if Location.objects.filter(coordinates=coordinates, city=city, name=name, slug__contains=name).exists():
            loc = Location.objects.get(coordinates=coordinates, city=city, name=name, slug__contains=name)
        else:
            loc = Location.objects.create(name=name, coordinates=coordinates, visited_by=str(current_user.id), city=city)
            loc.save()
        # now save the picture and review
        new_pic = Picture.objects.create(upload_date=datetime.date.today(), location_id=loc, uploaded_by=UserProfile.objects.get(user=current_user), picture=File(image, 'rb'))
        new_pic.save()
        new_review = Review.objects.create(title=title, publish_date=datetime.date.today(), content=content, rating=rating, location_id=loc, posted_by=UserProfile.objects.get(user=current_user))
        new_review.save()
        return HttpResponse(JsonResponse({
            'statusCode': 0,
            'message': '/advisor/location/' + loc.slug
        }))
    else:
        return render(request, 'advisor/add_location.html', context_dict)


@login_required
def toggle_visited(request):
    # for when the user clicks on a button to say if they have been in the location or not
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():
        # get the post fields from the request
        location_id = request.POST.get('location_id')
        state = request.POST.get('state')
        location = Location.objects.get(id=location_id)
        if location:
            visited_by_array = location.visited_by_list()
            user = str(request.user.id)
            if user in visited_by_array:
                visited_by_array.remove(user)  # remove the user from the visited by array
            else:
                visited_by_array.append(user)  # add the user to the visited by array
            location.visited_by = ",".join(visited_by_array)
            location.save()
            resp['statusCode'] = 0
    # not a POST request or something happened with the request
    else:
        resp['response type'] = 'not post: ' + str(request.method)
    return HttpResponse(JsonResponse(resp))


def location_details(request, location_name_slug):
    # get details about a location
    context_dict = {}
    try:
        location = Location.objects.get(slug=location_name_slug)
        comments = Review.objects.filter(location_id=location.pk)
        pictures = Picture.objects.filter(location_id=location.pk)
        visited_by_array = location.visited_by.split(",")
        no_visits = len(visited_by_array)

        # see if the user has visited the current place
        if request.user.is_authenticated():
            if str(request.user.id) in visited_by_array:
                visited_by_user = True
            else:
                visited_by_user = False
        else:
            visited_by_user = None

        # populate the context dict with appropriate info
        context_dict['comments'] = comments
        context_dict['pictures'] = pictures
        context_dict['location'] = location
        context_dict['num_pictures'] = range(len(pictures))
        context_dict['num_comments'] = range(len(comments))
        context_dict['slug'] = location_name_slug
        context_dict['no_visits'] = no_visits
        context_dict['visited_by_user'] = visited_by_user
    except Location.DoesNotExist:
        # if location does not exist, then everything is none. should not get here
        context_dict['comments'] = None
        context_dict['pictures'] = None
        context_dict['location'] = None
        context_dict['num_comments'] = None
        context_dict['num_pictures'] = None
        context_dict['slug'] = None
        context_dict['no_visits'] = None
        context_dict['visited_by_user'] = None
    return render(request, 'advisor/location_details.html', context_dict)


@login_required
def user_logout(request):
    # since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))


def register(request):
    # register a user
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():  # we are doing modal login so should only be ajax
        # get username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username__iexact=username).exists():  # see if user exists or not
            user = User.objects.create_user(username=username, password=password)
            profile = UserProfile.objects.create(user=user, avatar=File(open(os.path.join(settings.STATIC_DIR, 'images', 'default_avatar.png'), 'rb'), 'rb'))
            profile.save()
            # login user
            login(request, user)
            resp['statusCode'] = 0
            resp['currentUrl'] = request.POST.get('currentUrl')
    else:
        return redirect(reverse('index'))  # redirect user to index page if they try to access the url manually
        # resp['response type'] = 'not post: ' + str(request.method)
    return HttpResponse(JsonResponse(resp))


def user_login(request):
    # login a user
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():  # we are doing modal login so should only be ajax
        # get fields from post request
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                resp['statusCode'] = 0
                resp['currentUrl'] = request.POST.get('currentUrl')
        else:
            resp['details'] = "bad login details"
    else:
        return redirect(reverse('index'))  # redirect user to index page if they try to access the url manually
        # resp['response type'] = 'not post: ' + str(request.method)
    return HttpResponse(JsonResponse(resp))


@login_required
def write_review(request):
    # write a review
    resp = {'statusCode': 1}
    if request.method == 'POST':
        # get the post request fields
        title = request.POST.get('reviewTitle')
        rating = request.POST.get('input-rating')
        content = request.POST.get('reviewContent')
        slug = request.POST.get("slug")
        if title and rating and content:
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")

            location = Location.objects.get(slug=slug)
            user_profile = UserProfile.objects.get(user=request.user)
            
            review = Review.objects.create(title=title, publish_date=now, content=content,
                                           location_id=location, rating=rating,
                                           posted_by=user_profile)
            review.save()
            resp['statusCode'] = 0
            resp['currentUrl'] = request.POST.get('currentUrl')
    else:
        resp['response type'] = 'not post: ' + str(request.method)
    return HttpResponse(JsonResponse(resp))


def profile(request):
    # show the user's profile
    # if there is no logged in user, then redirect to index
    if not request.user.is_authenticated:
        return redirect(reverse('index'))
    context_dict = {}
    visited_locations = Location.objects.all().filter(visited_by__contains=request.user.id)
    context_dict['locations'] = visited_locations
    context_dict['count'] = len(visited_locations)
    return render(request, 'advisor/profile.html', context_dict)


@login_required()
def change_pw(request):
    # change the user's password
    resp = {"statusCode": 1}  # by default assume that it failed. as always you should
    if request.method == 'POST' and request.is_ajax():
        # get the new password
        new_password = request.POST.get('changePWPassword')
        user = User.objects.get(username=request.user.username)  # get the current user
        # change the password
        user.set_password(new_password)
        user.save()
        resp['statusCode'] = 0
    return HttpResponse(JsonResponse(resp))


@login_required()
def change_pp(request):
    # change the user's avatar
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():
        user = UserProfile.objects.get(user=request.user)
        # get the new avatar
        image = request.FILES.get('newAvatar')
        user.avatar = image
        # change the avatar
        user.save(update_fields=['avatar'])
        resp['statusCode'] = 0
    return HttpResponse(JsonResponse(resp))


@login_required()
def delete_account(request):
    # delete the user's account
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():
        current_user = User.objects.get(username=request.user.username)
        current_user_profile = UserProfile.objects.get(user=current_user)
        # logout the user just in case
        logout(request)
        # remove the user and their profile
        current_user.delete()
        current_user_profile.delete()
        resp['statusCode'] = 0
    return HttpResponse(JsonResponse(resp))


@login_required()
def upload_location_photo(request):
    # upload a new photo for the current location that is being viewed
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():
        # get the fields from the post request
        slug = request.POST.get("location")
        location = Location.objects.get(slug=slug)
        user_prof = UserProfile.objects.get(user=request.user)
        image = request.FILES.get('photo')
        new_pic = Picture.objects.create(location_id=location, uploaded_by=user_prof, picture=image)
        new_pic.save()
        resp['statusCode'] = 0
        resp['url'] = new_pic.picture.url
    return HttpResponse(JsonResponse(resp))


# helper method for title casing and taking care of apostrophes for when saving some of the fields
def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(), s)
