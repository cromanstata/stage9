
from .models import Recipe
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators import csrf

def cook_list(request):
    recipe_list = Recipe.objects.order_by('-publish_date')[:12]
    context = {'recipe_list': recipe_list}
    return render(request, 'cooks/cooks_list.html', context)


def cook_detail(request, recipe_title):
    recipe = get_object_or_404(Recipe, title=recipe_title)
    return render(request, 'cooks/cook_detail.html', {'recipe': recipe})


#def cook_search(request):
#    if request.method == "POST":
#       search_text = request.POST['search_text']
#    else:
#        search_text = ''
#    recipe_list = Recipe.objects.filter(title__contains=search_text)
#    context = {'recipe_list': recipe_list}
#    return render(request, 'cooks/cooks_search.html', context)
