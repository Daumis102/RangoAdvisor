from django.shortcuts import render
from advisor.forms import UserForm
#from advisor.forms import UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

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

def user_login(request):
    print("we are in a view!")
    # if the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'ajax':
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
                    'is_active': false
                }
                # an inactive account was used - no logging in!
                return HttpResponse(data, content_type='application/json')
        else:
            # Bad login credentials were provided. So we can't log the user in.
            data = {
                    'is_valid': false
                }
            return JsonResponse(data)
    else:
        return HttpResponse("Not a post request")
