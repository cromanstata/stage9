from django.shortcuts import get_object_or_404, render
from .forms import MyLoginForm
from django.contrib.auth.models import User
from profiles.forms import UserForm
from django.forms.models import inlineformset_factory
from profiles.models import UserProfile
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile
from profiles.forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


@login_required() # only logged in users should access this


def edit_user(request, name):
    # querying the User object with pk from url
    user = get_object_or_404(User, username=name)
    pk = request.user.pk

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('website', 'bio', 'phone', 'city', 'country', 'organization'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('/accounts/profile/')

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset
        })
    else:
        raise PermissionDenied

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
