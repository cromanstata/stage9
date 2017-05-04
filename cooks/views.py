
from .models import Recipe
from django.shortcuts import get_object_or_404, render


def cook_list(request):
    recipe_list = Recipe.objects.order_by('-publish_date')[:12]
    context = {'recipe_list': recipe_list}
    return render(request, 'cooks/cooks_list.html', context)


def cook_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'cooks/cook_detail.html', {'recipe': recipe})
