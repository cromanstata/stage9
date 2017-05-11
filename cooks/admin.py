
from django.contrib import admin
from .models import Recipe, Ingredient, Difficulty, Cuisine, MealType, WorkingTime, CookingTime
from django.utils.translation import ugettext_lazy as _

class CookingTimeInline(admin.TabularInline):
    model = CookingTime

class WorkingTimeInline(admin.TabularInline):
    model = WorkingTime

class MealTypeInline(admin.TabularInline):
    model = MealType

class CuisineInline(admin.TabularInline):
    model = Cuisine

class DifficultyInline(admin.TabularInline):
    model = Difficulty

class IngredientInline(admin.TabularInline):
    model = Ingredient

#class RecipeInline(admin.TabularInline):
#    model = Recipe
"""
class CuisineFilter(admin.SimpleListFilter):
    title = _('cuisine') # or use _('country') for translated title
    parameter_name = 'recipe'

    def lookups(self, request, model_admin):
        recipe = model_admin.model.objects.filter(id__in = Cuisine.objects.all().values_list('id', flat = True).distinct())
        return [(c.id, c) for c in recipe]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(recipe__id__exact=self.value())
        else:
            return ["not"]
"""
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')
    inlines = (IngredientInline, DifficultyInline, CuisineInline, MealTypeInline, WorkingTimeInline, CookingTimeInline)

    list_filter = ['publish_date',]
    search_fields = ['title']

admin.site.register(Recipe, RecipeAdmin)