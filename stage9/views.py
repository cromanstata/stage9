from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile
from friendship.models import Friend, Follow
from profiles.forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from cooks.models import Recipe, Ingredient, Favorite, MealType
from django.db.models import Q
import json
from django.http import HttpResponse
from cooks import fields
from cooks.forms import RecipeForm, IngredientForm, DifficultyForm, MealTypeForm, CuisineForm, CookingTimeForm
from django.utils import timezone
from notify.signals import notify


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
        search_title = request.POST['search_title']
        search_diff = request.POST['search_diff']
        search_cuisine = request.POST['search_cuisine']
        search_mealtype = request.POST['search_mealtype']
    else:
        search_text = ''
        search_title = ''
        search_diff = ''
        search_cuisine = ''
        search_mealtype = ''
    print (search_title)
    terms_entered = True
    filters = [search_diff, search_cuisine, search_mealtype]
    results=[]
    search2 = Q()
    search_text = search_text.split(',')
    recipe_list_search=''
    #if no ingredient tags where NOT searched:
    print ("search diff: ", search_diff)
    print("search_cuisine: ", search_cuisine)
    print("search_mealtype: ", search_mealtype)
    print("search_title: ", search_title)
    # if no ingredient tags where NOT searched AND title was NOT entered:
    if (isinstance(search_text, list) and search_text[0]=='' and search_title==''):
        if search_cuisine and search_cuisine != 'all' and search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
        else:
            if search_cuisine and search_cuisine != 'all' and search_mealtype and search_mealtype != 'all':
                recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype))
            else:
                if search_cuisine and search_cuisine != 'all' and search_diff and search_diff != 'all':
                    recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(difficulty__difficulty__iexact=search_diff))
                else:
                    if search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                        recipe_list_search = (Q(meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
                    else:
                        if search_diff and search_diff != 'all':
                            recipe_list_search = (Q(difficulty__difficulty__iexact=search_diff))
                        else:
                            if search_mealtype and search_mealtype != 'all':
                                recipe_list_search = (Q(meal_type__mealtype__iexact=search_mealtype))
                            else:
                                if search_cuisine and search_cuisine != 'all':
                                    recipe_list_search = (Q(cuisine__cuisine__iexact=search_cuisine))
        if recipe_list_search:
            f_search = Recipe.objects.filter(recipe_list_search).distinct()
            for recipe in f_search:
                results.append(str(recipe.id))
        else:
            if (search_cuisine == 'all') or (search_mealtype == 'all') or (search_diff == 'all'):
                print("there is nothing to show BUT CHOSE ALL")
                f_search= Recipe.objects.order_by('publish_date')[:20]
            else:
                f_search=''
                terms_entered = False
                print("there is nothing to show REALLY NOTHING")
            request.session['search_titles from_results'] = ""
            context = {'recipe_list_search': f_search,
                       'terms_entered': terms_entered}
            return render(request, 'stage9/ajax_search.html', context)
    #if no ingredient tags but title WAS entered
    if (isinstance(search_text, list) and search_text[0]=='' and search_title!=''):
        print("found title was entered")
        if search_cuisine and search_cuisine != 'all' and search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                recipe_list_search = (Q(title__icontains=search_title)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
        else:
            if search_cuisine and search_cuisine != 'all' and search_mealtype and search_mealtype != 'all':
                recipe_list_search = (Q(title__icontains=search_title)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype))
            else:
                if search_cuisine and search_cuisine != 'all' and search_diff and search_diff != 'all':
                    recipe_list_search = (Q(title__icontains=search_title)) &(Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(difficulty__difficulty__iexact=search_diff))
                else:
                    if search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                        recipe_list_search = (Q(title__icontains=search_title)) & (Q(meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
                    else:
                        if search_diff and search_diff != 'all':
                            recipe_list_search = (Q(title__icontains=search_title)) & (Q(difficulty__difficulty__iexact=search_diff))
                        else:
                            if search_mealtype and search_mealtype != 'all':
                                recipe_list_search = (Q(title__icontains=search_title)) & (Q(meal_type__mealtype__iexact=search_mealtype))
                            else:
                                if search_cuisine and search_cuisine != 'all':
                                    recipe_list_search = (Q(title__icontains=search_title)) & (Q(cuisine__cuisine__iexact=search_cuisine))
                                else:
                                    recipe_list_search = (Q(title__icontains=search_title))

        if recipe_list_search:
            f_search = Recipe.objects.filter(recipe_list_search).distinct()
            for recipe in f_search:
                results.append(str(recipe.id))
        else:
            f_search=''
            terms_entered = False
            print("there is nothing to show REALLY NOTHING")
            request.session['search_titles from_results'] = f_search
            context = {'recipe_list_search': f_search,
                       'terms_entered': terms_entered}
            return render(request, 'stage9/ajax_search.html', context)
    # if ingredient tags WHERE searched:
    else:
        if search_title=='':
            for title_ing in search_text:
                if search_cuisine and search_cuisine != 'all' and search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                        recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(
                            meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
                else:
                    if search_mealtype and search_mealtype != 'all' and search_cuisine and search_cuisine != 'all':
                        recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype))
                    else:
                        if search_cuisine and search_cuisine != 'all' and search_diff and search_diff != 'all':
                            recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(difficulty__difficulty__iexact=search_diff))
                        else:
                            if search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                                recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
                            else:
                                if search_diff and search_diff != 'all':
                                    recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(difficulty__difficulty__iexact=search_diff))
                                else:
                                    if search_mealtype and search_mealtype!='all':
                                        recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(meal_type__mealtype__iexact=search_mealtype))
                                    else:
                                        if search_cuisine and search_cuisine!='all':
                                            recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing)) & (Q(cuisine__cuisine__iexact=search_cuisine))
                                        else:
                                            recipe_list_search = (Q(ingredients__ingredient__iexact=title_ing))
                f_search = Recipe.objects.filter(recipe_list_search).distinct()
                for recipe in f_search:
                    results.append(str(recipe.id))
        else:
            for title_ing in search_text:
                if search_cuisine and search_cuisine != 'all' and search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                    recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                    Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(
                        meal_type__mealtype__iexact=search_mealtype)) & (Q(difficulty__difficulty__iexact=search_diff))
                else:
                    if search_mealtype and search_mealtype != 'all' and search_cuisine and search_cuisine != 'all':
                        recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                        Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(meal_type__mealtype__iexact=search_mealtype))
                    else:
                        if search_cuisine and search_cuisine != 'all' and search_diff and search_diff != 'all':
                            recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                            Q(cuisine__cuisine__iexact=search_cuisine)) & (Q(difficulty__difficulty__iexact=search_diff))
                        else:
                            if search_mealtype and search_mealtype != 'all' and search_diff and search_diff != 'all':
                                recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                                Q(meal_type__mealtype__iexact=search_mealtype)) & (
                                                     Q(difficulty__difficulty__iexact=search_diff))
                            else:
                                if search_diff and search_diff != 'all':
                                    recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                                    Q(difficulty__difficulty__iexact=search_diff))
                                else:
                                    if search_mealtype and search_mealtype != 'all':
                                        recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                                        Q(meal_type__mealtype__iexact=search_mealtype))
                                    else:
                                        if search_cuisine and search_cuisine != 'all':
                                            recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing)) & (
                                            Q(cuisine__cuisine__iexact=search_cuisine))
                                        else:
                                            recipe_list_search = (Q(title__icontains=search_title)) & (Q(ingredients__ingredient__iexact=title_ing))
                f_search = Recipe.objects.filter(recipe_list_search).distinct()
                for recipe in f_search:
                    results.append(str(recipe.id))

    for ids in results:
        if results.count(ids) == len(search_text):
            search2 = search2 | (Q(id=ids))
    if len(search2) != 0:
        f_search = Recipe.objects.filter(search2).distinct()
        json_titles = Recipe.objects.filter(search2).values('title').distinct()
        json_items = json.dumps(list(json_titles))
        print ("passed new value to title autocomplete")
        print (json_items)
        #request.session['title_before_search'] = False
        request.session['search_titles from_results'] = json_items
    else:
        f_search=''
        request.session['search_titles from_results'] = f_search
    context = {'recipe_list_search': f_search,
               'terms_entered': terms_entered}
    return render(request, 'stage9/ajax_search.html', context)

def allauthpop(request):
    if request.method == "GET":
        allauth_data = request.GET['allauth_data']
    else:
        allauth_data = ''
    #allauth_data can be either 'login' or 'register'
    context = {'recipe_list': allauth_data}
    return render(request, 'stage9/login_modal.html',context)


def get_tags(request):
    if request.method == "GET":
        search_tags = request.GET['term']
    else:
        search_tags = ''
    json_tags = Ingredient.objects.filter(ingredient__istartswith=search_tags).values('ingredient').distinct()
    json_items = json.dumps(list(json_tags))
    return HttpResponse(json_items, content_type='application/json')


def get_titles(request):
    results = []
    search2 = Q()
    recipe_list_search =''
    print ("reched view auto complete title")
    if request.method == "GET":
        search_titles = request.GET['term']
    else:
        search_titles = ''
    #title_before_search = request.session.get('title_before_search', True)
    json_titles_from_search = request.session.get('search_titles from_results', '')
    print("what autocomplete got:")
    print (json_titles_from_search)
    if json_titles_from_search:
        cond = json.loads(json_titles_from_search)
        for item in cond:
            title=(item['title'])
            search2 = search2 | (Q(title__iexact=title))
        f_search = Recipe.objects.filter(search2).distinct()
        json_titles = f_search.filter(title__icontains=search_titles).values('title').distinct()
        json_items = json.dumps(list(json_titles))
        #request.session['title_before_search'] = False
        return HttpResponse(json_items, content_type='application/json')
    else:
        json_titles = Recipe.objects.filter(title__icontains=search_titles).values('title').distinct()
        json_items = json.dumps(list(json_titles))
        return HttpResponse(json_items, content_type='application/json')


def get_diff_tags(request):
    if request.method == "GET":
        search_tags = request.GET['term']
    else:
        search_tags = ''
    if search_tags == "all":
        json_tags = Ingredient.objects.all().values('ingredient', 'slug').distinct()
        json_items = json.dumps(list(json_tags))
        return HttpResponse(json_items, content_type='application/json')
    else:
        json_tags = Ingredient.objects.filter(ingredient__iexact=search_tags).values('ingredient', 'slug').distinct()
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

def my_recipes(request, name):
    userq = get_object_or_404(User, username=name)
    # MY RECIPES: (request.user) - IM A REGISTERED USER LOOKING AT MY RECIPES
    if request.user.is_authenticated and request.user == userq:
        my_ids = Recipe.objects.filter(author_id=userq.id).distinct()
        if my_ids:
            d_search = my_ids
        else:
            d_search=''
        context = {'recipe_list': d_search,
                   'can_edit': True,
                   'user': userq}
        return render(request, 'cooks/my_recipes.html', context)
    # IM REGISTERED USER LOOKING AT SOMEONE ELSES LIST OF RECIPES -- OR IM NOT REGISTERED
    else:
        my_ids = Recipe.objects.filter(author_id=userq.id).distinct()
        if my_ids:
            d_search = my_ids
        else:
            d_search=''
        context = {'recipe_list': d_search,
                   'can_edit': False,
                   'user': userq}
        return render(request, 'cooks/my_recipes.html', context)

#RecipeForm, IngredientForm, DifficultyForm, MealTypeyForm, CuisineForm, WorkingTimeForm, CookingTimeForm

def add_recipe(request, name):
    nameid = str(request.user.id)
    user = get_object_or_404(User, username=name, id=nameid)
    recipe_form = RecipeForm(instance=user)
    ingredientInlineFormSet = inlineformset_factory(Recipe, Ingredient,
                                                    form=IngredientForm,
                                                    extra=3,
                                                    can_delete=True)
    ingredient_formset = ingredientInlineFormSet(prefix='fs1')
    mealTypeInlineFormSet=inlineformset_factory(Recipe, MealType,
                                                form=MealTypeForm, extra=1, can_delete=True)
    mealtype_formset = mealTypeInlineFormSet(prefix='fs2')
    difficulty_form = DifficultyForm(instance=recipe_form.instance)
    cuisine_form = CuisineForm(instance=recipe_form.instance)
    cookingtime_form = CookingTimeForm(prefix='cooking', instance=recipe_form.instance)


    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = ingredientInlineFormSet(request.POST, request.FILES, instance=recipe_form.instance,
                                                     prefix='fs1')
        mealtype_formset = mealTypeInlineFormSet(request.POST, request.FILES, instance=recipe_form.instance,
                                                     prefix='fs2')
        difficulty_form = DifficultyForm(request.POST)
        cuisine_form = CuisineForm(request.POST)
        cookingtime_form = CookingTimeForm(request.POST, prefix='cooking')
        print("recipe_form.is_valid()", recipe_form.is_valid())
        print("ingredient_formset.is_valid()", ingredient_formset.is_valid())
        print("mealtype_formset.is_valid()", mealtype_formset.is_valid())
        print("difficulty_form.is_valid()", difficulty_form.is_valid())
        print("cuisine_form.is_valid()", cuisine_form.is_valid())
        print("cookingtime_form.is_valid()", cookingtime_form.is_valid())
        if recipe_form.is_valid() and ingredient_formset.is_valid() and mealtype_formset.is_valid() and difficulty_form.is_valid() and cuisine_form.is_valid() and cookingtime_form.is_valid():
            recipe_post = recipe_form.save(commit=False)
            recipe_post.author = user
            recipe_post.publish_date = timezone.now()
            if recipe_post.photo:
                recipe_post.photo = request.FILES['photo']
            recipe_post.save()
            difficulty_post = difficulty_form.save(commit=False)
            difficulty_post.recipe_id = recipe_post.id
            cuisine_post = cuisine_form.save(commit=False)
            cuisine_post.recipe_id = recipe_post.id
            cookingtime_post = cookingtime_form.save(commit=False)
            cookingtime_post.recipe_id = recipe_post.id
            for form in ingredient_formset:
                data = form.cleaned_data
                print(data)
                try:
                    field = data['ingredient']
                except:
                    field = ''
                print(field, " name of the field")
                if form.is_valid() and field:
                    print(field, "SAVED")
                    form_post = form.save(commit=False)
                    form_post.recipe_id = recipe_post.id
                    form_post.save()
            for form in mealtype_formset:
                data = form.cleaned_data
                try:
                    field = data['mealtype']
                except:
                    field = ''
                if form.is_valid() and field:
                    form_post = form.save(commit=False)
                    form_post.recipe_id = recipe_post.id
                    form_post.save()
            #ingredient_formset.save()
            #mealtype_formset.save()
            difficulty_post.save()
            cuisine_post.save()
            cookingtime_post.save()
            followers = Follow.objects.followers(user)
            if followers:
                notify.send(user, actor=user, recipient_list=followers, verb='posted a new recipe', target=recipe_post)
            return redirect('cooks:detail', recipe_post.title)
        else:
            print ("one of the forms was not valid?")
            context = {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset,
                       'difficulty_form': difficulty_form, 'cuisine_form': cuisine_form,
                       'cookingtime_form': cookingtime_form,
                       'mealtype_formset' :mealtype_formset, 'user': user}
            return render(request, 'cooks/add_recipe.html', context)

    else:
        context = {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset,
                   'difficulty_form': difficulty_form, 'cuisine_form': cuisine_form,
                   'cookingtime_form': cookingtime_form,
                   'mealtype_formset': mealtype_formset, 'user': user}
        return render(request, 'cooks/add_recipe.html', context)

