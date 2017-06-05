from cooks.models import Recipe, Ingredient
from slugify import slugify

for obj in Recipe.objects.filter(slug=""):
    obj.slug = slugify(obj.title)
    obj.save()

for obj in Ingredient.objects.filter(slug=""):
    obj.slug = slugify(obj.ingredient)
    obj.save()
