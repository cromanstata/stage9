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
            ingredient_formset.save()
            mealtype_formset.save()
            difficulty_post.save()
            cuisine_post.save()
            cookingtime_post.save()
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

