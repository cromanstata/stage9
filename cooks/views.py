
from .models import User, Recipe, Favorite, Like, Ingredient, MealType, Difficulty, Cuisine, WorkingTime, CookingTime
from django.shortcuts import get_object_or_404, render, redirect
from cooks.forms import RecipeForm, IngredientForm, DifficultyForm, MealTypeForm, CuisineForm, WorkingTimeForm, CookingTimeForm
from django.utils import timezone
from django.forms.models import inlineformset_factory

def cook_list(request):
    recipe_list = Recipe.objects.order_by('-publish_date')[:12]
    context = {'recipe_list': recipe_list}
    return render(request, 'cooks/cooks_list.html', context)


def cook_detail(request, recipe_title):
    recipe = get_object_or_404(Recipe, title=recipe_title)
    try:
        author = User.objects.get(id=recipe.author_id)
    except:
        author = ''
    is_favorite = False
    is_liked = False
    #IF REGISTERED USER LOOKING - check if already favors or likes the recipe
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.favors(request.user, recipe)
        is_liked = Like.objects.likes(request.user, recipe)
    # IF ALL USERS ARE LOOKING - show counters for likes and favourites
    favorers = Favorite.objects.favorers(recipe)
    #likes = int(Like.objects.get_likes(recipe.id))
    likes = Like.objects.get_likes(recipe)
    return render(request, 'cooks/cook_detail.html', {'recipe': recipe,
                                                      'is_favorite': is_favorite,
                                                      'is_liked': is_liked,
                                                      'likes': likes,
                                                      'favorers': favorers,
                                                      'author': author})

def favorite(request):
    if request.method == "GET":
        recipe_view = request.GET['recipe_view']
        action = request.GET['action']
    else:
        recipe_view = ''
        action = ''
    recipe = get_object_or_404(Recipe, title=recipe_view)
    if action == 'favorite':
        Favorite.objects.add_favorite(request.user, recipe)
        return render(request, 'cooks/favorite_form.html')

    if action == 'unfavor':
        Favorite.objects.remove_favorite(request.user, recipe)
        return render(request, 'cooks/favorite_form.html')


def like(request):
    if request.method == "GET":
        recipe_view = request.GET['recipe_view']
        action = request.GET['action']
    else:
        recipe_view = ''
        action = ''
    recipe = get_object_or_404(Recipe, title=recipe_view)
    if action == 'like':
        Like.objects.add_like(request.user, recipe)
        return render(request, 'cooks/like_form.html')

    if action == 'unlike':
        Like.objects.remove_like(request.user, recipe)
        return render(request, 'cooks/like_form.html')


def edit_recipe(request, recipe_title):
    user = request.user
    recipe = get_object_or_404(Recipe, title=recipe_title, author_id=user.id)
    recipe_form = RecipeForm(instance=recipe)
    try:
        difficulty = Difficulty.objects.get(recipe_id=recipe.id)
        difficulty_form = DifficultyForm(instance=difficulty)
    except:
        difficulty_form = DifficultyForm(instance=recipe)
    try:
        cuisine = Cuisine.objects.get (recipe_id=recipe.id)
        cuisine_form = CuisineForm(instance=cuisine)
    except:
        cuisine_form = CuisineForm(instance=recipe)
    try:
        workingtime = WorkingTime.objects.get(recipe_id=recipe.id)
        workingtime_form = WorkingTimeForm(prefix='working', instance=workingtime)
    except:
        workingtime_form = WorkingTimeForm(prefix='working',instance=recipe)
    try:
        cookingtime = CookingTime.objects.get(recipe_id=recipe.id)
        cookingtime_form = CookingTimeForm(prefix='cooking', instance=cookingtime)
    except:
        cookingtime_form = CookingTimeForm(prefix='cooking', instance=recipe)
    ingredientInlineFormSet = inlineformset_factory(Recipe, Ingredient,
                                                    fields=('ingredient', 'quantity', 'unit', 'note'),
                                                    extra=3,
                                                    can_delete=True,
                                                    )
    ingredient_formset = ingredientInlineFormSet(prefix='fs1', instance=recipe)
    mealTypeInlineFormSet = inlineformset_factory(Recipe, MealType,
                                                  fields=('mealtype',),
                                                  extra=1,
                                                  can_delete=True)
    mealtype_formset = mealTypeInlineFormSet(prefix='fs2', instance=recipe)
    #works up to here
    if request.method == "POST":
        if request.POST.get('delete'):
            print("got delete command")
            recipe.delete()
            return redirect('profiles:my_recipes')
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = ingredientInlineFormSet(request.POST, request.FILES, instance=recipe_form.instance, prefix='fs1')
        mealtype_formset = mealTypeInlineFormSet(request.POST, request.FILES, instance=recipe_form.instance, prefix='fs2')
        try:
            difficulty = Difficulty.objects.get(recipe_id=recipe.id)
            difficulty_form = DifficultyForm(request.POST, instance=difficulty)
        except:
            difficulty_form = DifficultyForm(request.POST, instance=recipe)
        try:
            cuisine = Cuisine.objects.get(recipe_id=recipe.id)
            cuisine_form = CuisineForm(request.POST, instance=cuisine)
        except:
            cuisine_form = CuisineForm(request.POST, instance=recipe)
        try:
            workingtime = WorkingTime.objects.get(recipe_id=recipe.id)
            workingtime_form = WorkingTimeForm(request.POST, prefix='working', instance=workingtime)
            print("should be saving working time")
        except:
            print ("except for working time")
            workingtime_form = WorkingTimeForm(request.POST, prefix='working', instance=recipe)
        try:
            cookingtime = CookingTime.objects.get(recipe_id=recipe.id)
            cookingtime_form = CookingTimeForm(request.POST, prefix='cooking', instance=cookingtime)
            print("should be saving cooking time")
        except:
            print("except for cooking time time")
            cookingtime_form = CookingTimeForm(request.POST, prefix='cooking', instance=recipe)
        if recipe_form.is_valid() and ingredient_formset.is_valid() and mealtype_formset.is_valid() and difficulty_form.is_valid() and cuisine_form.is_valid() and workingtime_form.is_valid() and cookingtime_form.is_valid():
            recipe_post = recipe_form.save(commit=False)
            recipe_post.author = user
            recipe_post.publish_date = timezone.now()
            #if recipe_post.photo:
            #    print("adding photo?")
            #    recipe_post.photo = request.FILES['photo']
            #print("NOT adding photo?")
            difficulty_post = difficulty_form.save(commit=False)
            difficulty_post.recipe_id = recipe_post.id
            cuisine_post = cuisine_form.save(commit=False)
            cuisine_post.recipe_id = recipe_post.id
            workingtime_post = workingtime_form.save(commit=False)
            workingtime_post.recipe_id = recipe_post.id
            cookingtime_post = cookingtime_form.save(commit=False)
            cookingtime_post.recipe_id = recipe_post.id
            recipe_post.save()
            ingredient_formset.save()
            mealtype_formset.save()
            difficulty_post.save()
            cuisine_post.save()
            workingtime_post.save()
            cookingtime_post.save()
            # for post1 in ingredient_post:
            #    post1.recipe_id = recipe_post.id
            #    post1.save()
            return redirect('cooks:detail', recipe_post.title)
        else:
            context = {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset,
                       'difficulty_form': difficulty_form, 'cuisine_form': cuisine_form,
                       'workingtime_form': workingtime_form, 'cookingtime_form': cookingtime_form,
                       'mealtype_formset': mealtype_formset, 'user': user}
            return render(request, 'cooks/add_recipe.html', context)

    else:
        context = {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset,
                   'difficulty_form': difficulty_form, 'cuisine_form': cuisine_form,
                   'workingtime_form': workingtime_form, 'cookingtime_form': cookingtime_form,
                   'mealtype_formset': mealtype_formset, 'user': user}
        return render(request, 'cooks/add_recipe.html', context)