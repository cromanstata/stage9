from .forms import MyLoginForm, CousineForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile
from friendship.models import Friend, Follow
from profiles.forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from cooks.models import Recipe, Ingredient, Favorite
from django.db.models import Q
from itertools import chain
import json
from django.core import serializers
from django.http import HttpResponse
from cooks import fields


@login_required() # only logged in users should access this
def edit_user(request, name):
    # querying the User object with pk from url
    nameid = str(request.user.id)
    user = get_object_or_404(User, username=name, id=nameid)
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
    userq = get_object_or_404(User, username=name)
    #MY PROFILE: (request.user)
    if request.user.is_authenticated and request.user == userq:
        nameid = str(request.user.id)
        user = get_object_or_404(User, username=name, id=nameid)
        followers = Follow.objects.followers(user)
        return render(request, 'stage9/user.html', {'profile_view': user,
                                                    'followers': followers})
    # IM REGISTERED USER LOOKING AT SOMEONE ELSES PROFILE
    if request.user.is_authenticated:
        #DO OR SHOW STUFF RELATED
        is_following = Follow.objects.follows(request.user, userq)
        return render(request, 'stage9/user.html', {'profile_view': userq,
                                                    'is_following': is_following})
    # IM NOT REGISTERED AKA ANON LOOKING AT PROFILES
    else:
        #DO OR SHOW STUFF RELATED
        return render(request, 'stage9/user.html', {'profile_view': userq})


def home(request):
    context = {
        'fields': fields,
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
        search_cuisine = request.POST['search_cuisine']
        search_mealtype = request.POST['search_mealtype']
    else:
        search_text = ''
        search_cuisine = ''
        search_mealtype = ''
    results=[]
    search2 = Q()
    search_text = search_text.split(',')
    recipe_list_search=''
    #if no ingredient tags where searched:
    if (isinstance(search_text, list) and search_text[0]==''):
        if search_cuisine:
            if search_mealtype:
                recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype))
            else:
                recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine))
        if search_mealtype:
            if search_cuisine:
                recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype))
            else:
                recipe_list_search = (Q(meal_type__mealtype__iexact=search_mealtype))
        if recipe_list_search:
            f_search = Recipe.objects.filter(recipe_list_search).distinct()
            for recipe in f_search:
                results.append(str(recipe.id))
        else:
            f_search= Recipe.objects.order_by('publish_date')[:20]
            context = {'recipe_list_search': f_search}
            return render(request, 'stage9/ajax_search.html', context)
    # if ingredient tags where searched:
    else:
        for title_ing in search_text:
            if search_cuisine:
                if search_mealtype:
                    recipe_list_search = (Q(ingredients__ingredient__icontains=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(
                        meal_type__mealtype__iexact=search_mealtype))
                else:
                    recipe_list_search = (Q(ingredients__ingredient__icontains=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine))
            if search_mealtype:
                if search_cuisine:
                    recipe_list_search = (Q(ingredients__ingredient__icontains=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(
                        meal_type__mealtype__iexact=search_mealtype))
                else:
                    recipe_list_search = (Q(ingredients__ingredient__icontains=title_ing)) & (Q(meal_type__mealtype__iexact=search_mealtype))
            if not search_cuisine and not search_mealtype:
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


def follow(request):
    if request.method == "GET":
        profile_view = request.GET['profile_view']
        action = request.GET['action']
    else:
        profile_view = ''
        action = ''
    userq = User.objects.get(username=profile_view)
    if action == 'follow':
        Follow.objects.add_follower(request.user, userq)
        return render(request, 'stage9/follow_form.html')

    if action == 'unfollow':
        Follow.objects.remove_follower(request.user, userq)
        return render(request, 'stage9/follow_form.html')

def favorites(request, name):
    favorite_ids = Favorite.objects.filter(favorer_id=request.user.id).values('recipe_id').distinct()
    search3 = Q()
    if favorite_ids:
        for id in favorite_ids:
            i = (id['recipe_id'])
            search3 = search3 | (Q(favorite__recipe_id=i))
        d_search = Recipe.objects.filter(search3).distinct()
    else:
        d_search=''
    context = {'recipe_list': d_search}
    return render(request, 'cooks/favorite_list.html', context)


