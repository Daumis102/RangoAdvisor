from django.shortcuts import render
#from advisor.forms import UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from advisor.models import *
import datetime


# Create your views here.
def about(request):
    return render(request, 'advisor/about.html', context={})


def contacts(request):
    return render(request, 'advisor/contacts.html', context={})


def index(request):
    locations_list = Location.objects.order_by('-name')
    context_dict = {'locations': locations_list}
    return render(request, 'advisor/index.html', context_dict)


@login_required
def add_location(request):
    context_dict = {}
    if request.method == 'POST':  # will just post back to the same url but with data
        name = request.POST.get("name")
        coordinates = request.POST.get("coordinates")
    #     other items here
    else:
        return render(request, 'advisor/add_location.html', context_dict)

@login_required
def toggle_visited(request):
    if request.method == 'POST' and request.is_ajax():
        location_id=request.POST.get('location_id')
        state=request.POST.get('state')
        location = Location.objects.get(id=location_id)
        if location:
            visited_by_array = location.visited_by.split(",")
            user = str(request.user.id)
            try:
                if user in visited_by_array:
                    visited_by_array.remove(user)
                else:
                    visited_by_array.append(user)
                location.visited_by = ",".join(visited_by_array)
                location.save()
                print(location.visited_by)
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
    if request.method == 'POST' and request.is_ajax():  # we are doing modal login so should only be ajax
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username__iexact=username).exists():
            user = User.objects.create_user(username=username, password=password)
            profile = UserProfile.objects.create(user=user)
            # login user
            login(request, user)
            return HttpResponse(JsonResponse({
                'currentUrl': request.POST.get('currentUrl'),
                'statusCode': 0
            }))
        else:
            # Invalid form or forms - mistakes or something else?
            data = {
                    "statusCode": 1
            }
            return HttpResponse(JsonResponse(data))
    # not a POST request
    else:
        return HttpResponse(JsonResponse({
            "response type": "not post"
        }))


def user_login(request):
    if request.method == 'POST' and request.is_ajax():  # we are doing modal login so should only be ajax
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
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
                "details": "bad login details"
            }))

    else:
        return HttpResponse(JsonResponse({
            "response type": "not post"
        }))


@login_required
def write_review(request):
    print("WRITE REVIEW")
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



