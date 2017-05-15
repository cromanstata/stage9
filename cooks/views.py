
from .models import Recipe, Favorite, Like
from django.shortcuts import get_object_or_404, render

def cook_list(request):
    recipe_list = Recipe.objects.order_by('-publish_date')[:12]
    context = {'recipe_list': recipe_list}
    return render(request, 'cooks/cooks_list.html', context)


def cook_detail(request, recipe_title):
    recipe = get_object_or_404(Recipe, title=recipe_title)
    is_favorite = False
    #IF REGISTERED USER LOOKING
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.favors(request.user, recipe)
    # IF ALL USERS ARE LOOKING
    favorers = Favorite.objects.favorers(recipe)
    likes = int(Like.objects.get_likes(recipe.id))
    return render(request, 'cooks/cook_detail.html', {'recipe': recipe,
                                                      'is_favorite': is_favorite,
                                                      'likes': likes,
                                                      'favorers': favorers})

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
        Like.objects.add_like(recipe)
        return render(request, 'cooks/like_form.html')

    if action == 'unlike':
        Like.objects.remove_like(recipe)
        return render(request, 'cooks/like_form.html')