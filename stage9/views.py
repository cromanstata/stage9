from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import get_object_or_404, render
from profiles.models import UserProfile
from django.contrib.auth.models import User
from .forms import MyLoginForm
from allauth.account.views import *
from allauth.account.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def profile(request, name):
    user = get_object_or_404(User, username=name)
    return render(request, 'stage9/user.html', {'profile': user})

def home(request):
    context = {
        'login_form': MyLoginForm(),
    }
    return render(request, 'stage9/home.html', context)

# def profile(request):
    #user=UserProfile
    #name=request.user.username
    #return render(request, 'profiles/profile.html', {'profile': user})
    #return HttpResponseRedirect(reverse('profiles:profile', args=(name)))
