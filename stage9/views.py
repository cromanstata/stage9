from .forms import MyLoginForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile
from profiles.forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from cooks.models import Recipe, IngredientSearch, Ingredient
from django.db.models import Q
from itertools import chain
import json
from django.core import serializers
from django.http import HttpResponse


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
        #'formset': IngredientSearch()
    }
    return render(request, 'stage9/home.html', context)

def availble_tags (request):
    list_tags = ''
    if request.method == "GET":
        tags = Ingredient.objects.all().values('ingredient').distinct()
        list_tags = [d['ingredient'] for d in tags]
    else:
        tags = ''
    context = {'all_ingrident_tags': list_tags}
    return render(request, 'stage9/availble_tags.html', context)

def search(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    results=[]
    search2 = Q()
    search_text = search_text.split(',')

    if (isinstance(search_text, list) and search_text[0]==''):
        f_search=''
        context = {'recipe_list_search': f_search}
        return render(request, 'stage9/ajax_search.html', context)

    else:
        for title_ing in search_text:
            recipe_list_search = (Q(ingredients__ingredient__icontains=title_ing))
            f_search = Recipe.objects.filter(recipe_list_search).distinct()
            for recipe in f_search:
                results.append(str(recipe.id))
        for ids in results:
            if results.count(ids) == len(search_text):
                search2 = search2 | (Q(id=ids))
        if len(search2) != 0:
            f_search = Recipe.objects.filter(search2).distinct()
        else:
            f_search=''
        context = {'recipe_list_search': f_search}
        return render(request, 'stage9/ajax_search.html', context)

def get_tags(request):
    if request.method == "GET":
        search_tags = request.GET['term']
    else:
        search_tags = ''
    json_tags = Ingredient.objects.filter(ingredient__istartswith=search_tags).values('ingredient').distinct()
    json_items = json.dumps(list(json_tags))
    return HttpResponse(json_items, content_type='application/json')

def get_diff_tags(request):
    if request.method == "GET":
        search_tags = request.GET['term']
    else:
        search_tags = ''
    if search_tags == "all":
        json_tags = Ingredient.objects.all().values('ingredient').distinct()
        json_items = json.dumps(list(json_tags))
        return HttpResponse(json_items, content_type='application/json')