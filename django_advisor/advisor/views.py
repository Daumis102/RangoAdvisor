from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.files import File
from advisor.models import *
import datetime
import os


def about(request):
    return render(request, 'advisor/about.html', context={})


def contacts(request):
    return render(request, 'advisor/contacts.html', context={})


def index(request):
    context_dict = {}
    locations_list = Location.objects.order_by('-name')
    visited_places = []
    user = str(request.user.id)
    for location in locations_list: 
        if user in location.visited_by_list():
            visited_places.append(location)
    context_dict['locations'] = locations_list
    context_dict['visited_places'] = visited_places
    return render(request, 'advisor/index.html', context_dict)


@login_required
def add_location(request):
    context_dict = {}
    if request.method == 'POST' and request.is_ajax():  # will just post back to the same url but with data
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
    if request.method == 'POST' and request.is_ajax():
        location_id = request.POST.get('location_id')
        state = request.POST.get('state')
        location = Location.objects.get(id=location_id)
        if location:
            visited_by_array = location.visited_by_list()
            user = str(request.user.id)
            try:
                if user in visited_by_array:
                    visited_by_array.remove(user)
                else:
                    visited_by_array.append(user)
                location.visited_by = ",".join(visited_by_array)
                location.save()
                return HttpResponse(JsonResponse({
                            'statusCode': 0,
                        }))
            except:
                return HttpResponse(JsonResponse({
                            'statusCode': 1,
                        }))
        else:
            return HttpResponse(JsonResponse({
                    'statusCode': 1
                }))
    # not a POST request
    else:
        return HttpResponse(JsonResponse({
            "response type": "not post"
        }))


def location_details(request, location_name_slug):
    context_dict = {}
    try:
        location = Location.objects.get(slug=location_name_slug)
        comments = Review.objects.filter(location_id=location.pk)
        pictures = Picture.objects.filter(location_id=location.pk)
        visited_by_array = location.visited_by.split(",")
        no_visits = len(visited_by_array)

        if request.user.is_authenticated():
            if str(request.user.id) in visited_by_array:
                visited_by_user = True
            else:
                visited_by_user = False
        else:
            visited_by_user = None

        context_dict['comments'] = comments
        context_dict['pictures'] = pictures
        context_dict['location'] = location
        context_dict['num_pictures'] = range(len(pictures))
        context_dict['num_comments'] = range(len(comments))
        context_dict['slug'] = location_name_slug
        context_dict['no_visits'] = no_visits
        context_dict['visited_by_user'] = visited_by_user
    except Location.DoesNotExist:
        context_dict['comments'] = None
        context_dict['pictures'] = None
        context_dict['location'] = None
        context_dict['num_comments'] = None
        context_dict['num_pictures'] = None
        context_dict['slug'] = None
        context_dict['no_visits'] = None
        context_dict['visited_by_user'] = None
    return render(request, 'advisor/location_details.html', context_dict)


# use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    # since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))


def register(request):
    resp = {'statusCode': 0}
    if request.method == 'POST' and request.is_ajax():  # we are doing modal login so should only be ajax
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username__iexact=username).exists():
            user = User.objects.create_user(username=username, password=password)
            profile = UserProfile.objects.create(user=user, avatar=File(open(os.path.join(settings.STATIC_DIR, 'images', 'no-foto.png'), 'rb'), 'rb'))
            profile.save()
            # login user
            login(request, user)
            resp['statusCode'] = 0
            resp['currentUrl'] = request.POST.get('currentUrl')
    else:
        resp['response type'] = 'not post: ' + str(request.method)
    return HttpResponse(JsonResponse(resp))


def user_login(request):
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():  # we are doing modal login so should only be ajax
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
        resp['response type'] = 'not post: ' + str(request.method)
    return HttpResponse(JsonResponse(resp))


@login_required
def write_review(request):
    if request.method == 'POST':
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
            return HttpResponse(JsonResponse({
                'currentUrl': request.POST.get('currentUrl'),
                'statusCode': 0
            }))
        else:
            return HttpResponse(JsonResponse({
                "statusCode": 1
            }))

    else:
        return HttpResponse(JsonResponse({
            "response type": "not post"
        }))


def profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse('index'))
    context_dict = {}
    visited_locations = Location.objects.all().filter(visited_by__contains=request.user.id)
    context_dict['locations'] = visited_locations
    context_dict['count'] = len(visited_locations)
    return render(request, 'advisor/profile.html', context_dict)


@login_required()
def change_pw(request):
    resp = {"statusCode": 1}  # by default assume that it failed. as always you should
    if request.method == 'POST' and request.is_ajax():
        new_password = request.POST.get('changePWPassword')
        user = User.objects.get(username=request.user.username)  # get the current user
        user.set_password(new_password)
        user.save()
        resp['statusCode'] = 0
    return HttpResponse(JsonResponse(resp))


@login_required()
def change_pp(request):
    resp = {'statusCode': 1}
    if request.method == 'POST' and request.is_ajax():
        user = UserProfile.objects.get(user=request.user)
        image = request.FILES.get('newAvatar')
        user.avatar = image
        user.save(update_fields=['avatar'])
        resp['statusCode'] = 0
    return HttpResponse(JsonResponse(resp))


# helper method for title casing and taking care of apostrophes
def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(), s)
