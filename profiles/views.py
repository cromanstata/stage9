from django.shortcuts import get_object_or_404, render
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def profile(request):
    name=request.user.username
    return redirect('/' + name + '/')