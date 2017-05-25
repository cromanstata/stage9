from django import forms
from .models import Recipe, Ingredient, Difficulty, MealType, Cuisine, WorkingTime, CookingTime
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from . import fields
from django.utils.translation import ugettext_lazy as _


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'photo', 'summary', 'description', 'portions')

#IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('ingredient', 'quantity', 'unit', 'note'))


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('ingredient', 'quantity', 'unit', 'note')


class DifficultyForm(forms.ModelForm):
    class Meta:
        model = Difficulty
        fields = ('difficulty',)


class MealTypeForm(forms.ModelForm):
    class Meta:
        model = MealType
        fields = ('mealtype',)


class CuisineForm(forms.ModelForm):
    class Meta:
        model = Cuisine
        fields = ('cuisine',)


class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        fields = ('hours', 'minutes')


class CookingTimeForm(forms.ModelForm):
    class Meta:
        model = CookingTime
        fields = ('hours', 'minutes')


