
from django.contrib import admin
from .models import Recipe, Ingredient, Difficulty

class DifficultyInline(admin.TabularInline):
    model = Difficulty

class IngredientInline(admin.TabularInline):
    model = Ingredient

class RecipeInline(admin.TabularInline):
    model = Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')
    inlines = (IngredientInline, DifficultyInline)

admin.site.register(Recipe, RecipeAdmin)
#admin.site.register(Ingredient, RecipeAdmin)
#admin.site.register(Difficulty, RecipeAdmin)