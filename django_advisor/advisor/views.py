from django.shortcuts import render
from advisor.forms import UserForm
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

def index(request):
    return HttpResponse("index")
def add_place(request):
    return HttpResponse("add place")

# use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    # since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))

def register(request):
    # a boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # if its a HTTP POST we're interested in processing form data.
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        username = request.POST.get('username')
        print(user_form.is_valid())
        if not User.objects.filter(username__iexact=username).exists():
            user = User.objects.create_user(username=username,
                                 password=password)
            # login user
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # Invalid form or forms - mistakes or something else?
            # return json
            data = {
                    'error': True,
            }
            return JsonResponse(data)
    # not a POST request
    else:
        return HTTPResponse("not a POST request")



def user_login(request):
    print("we are in a view!")
    # if the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user
        # This information is obtained from the login form/
        # We user request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while other will raise a KeyError exception.
    
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is
        user = authenticate(username=username, password=password)

        # if we have a User object, the details are correct.
        # if None, no user with matching credentials was found

        if user:
            # Is the account active? It could have been dissabled.
            if user.is_active:
                # if the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                data = {
                    'is_active': False,
                }
                # an inactive account was used - no logging in!
                return JsonResponse(data)
        else:
            # Bad login credentials were provided. So we can't log the user in.
            data = {
                    'is_valid': False,
                }
            return JsonResponse(data)
    else:
        return HttpResponse("Not a post request")
