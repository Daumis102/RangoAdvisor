from django.shortcuts import render
from advisor.forms import LoginForm
#from advisor.forms import UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.models import User


# Create your views here.
def about(request):
    return render(request, 'advisor/about.html', context={})


def index(request):  # TODO: make this return the index page when that is finished

    return render(request, 'advisor/index.html', context={})


def add_place(request):  # TODO: make this return the add_place page when that is finished
    return HttpResponse("add place")


# use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    # since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    username = ''
    password = ''
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(user_form.is_valid())
        if not User.objects.filter(username__iexact=username).exists():
            user = User.objects.create_user(username=username, password=password)
            # login user
            login(request, user)
            return HttpResponse(JsonResponse({
                "registration": True
            }))
        else:
            # Invalid form or forms - mistakes or something else?
            # return json
            data = {
                    'registration': False,
            }
            return HttpResponse(JsonResponse(data))
    # not a POST request
    else:
        return HttpResponse(JsonResponse({
            "response type": "not post"
        }))


def user_login(request):
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponse(JsonResponse({
                    'login': True
                }))
            else:
                return HttpResponse(JsonResponse({
                    "login": False
                }))

        else:
            return HttpResponse(JsonResponse({
                "details": "bad login details"
            }))

    else:
        return HttpResponse(JsonResponse({
            "response type": "not post"
        }))
