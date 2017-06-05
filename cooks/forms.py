from django import forms
from .models import Recipe, Ingredient, Difficulty, MealType, Cuisine, WorkingTime, CookingTime
from django.forms.formsets import BaseFormSet
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from . import fields
from django.utils.translation import ugettext_lazy as _
from .widgets import ClearableIMGInput2


class RecipeForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title_css'}))
    summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'summary_css'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'description_css'}))
    portions = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'portions_css'}))
    photo = forms.ImageField(required=False, widget=ClearableIMGInput2(attrs={'class': 'photo_css',
                                                             'onchange': 'upload_img(this);'}))

    # .NumberInput(attrs={'step': 0.5}))

    class Meta:
        model = Recipe
        fields = ('title', 'photo', 'summary', 'description', 'portions')
        labels = {
            "title": "TITLE",
            "photo": "IMAGE",
            "summary": "SUMMERY",
            "description": "INSTRUCTIONS",
            "portions": "PORTIONS"
        }

#IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('ingredient', 'quantity', 'unit', 'note'))


class IngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)

        self.fields['ingredient'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'ingredient_formset_css'
            }))
        self.fields['quantity'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'quantity_formset_css'
        }))
        self.fields['note'] = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'note_formset_css'
        }))
        self.fields['unit'] = forms.CharField(required=False, widget=forms.Select(attrs={
            'class': 'unit_formset_css',
        }, choices=(('', ''),)+fields.UNITS))


    class Meta:
        model = Ingredient
        fields = ('ingredient', 'quantity', 'unit', 'note')


class BaseIngredientFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        ingredient = []
        quantity = []
        unit = []
        note = []

        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                ingredient = form.cleaned_data['ingredient']
                quantity = form.cleaned_data['quantity']
                unit = form.cleaned_data['unit']
                note = form.cleaned_data['note']
                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                    )


class DifficultyForm(forms.ModelForm):

    difficulty = forms.CharField(required=False, widget=forms.Select(attrs={
        'class': 'difficulty_css',
    }, choices=(('', ''),) + fields.DIFFICULTIES))

    class Meta:
        model = Difficulty
        fields = ('difficulty',)


class MealTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MealTypeForm, self).__init__(*args, **kwargs)

        self.fields['mealtype'] = forms.CharField(required=False, widget=forms.Select(attrs={
            'class': 'mealtype_css',
        }, choices=(('', ''),) + fields.MEALTYPE))


    class Meta:
        model = MealType
        fields = ('mealtype',)


class CuisineForm(forms.ModelForm):
    cuisine = forms.CharField(required=False, widget=forms.Select(attrs={
        'class': 'cuisine_css',
    }, choices=(('', ''),) + fields.CUISINE))

    class Meta:
        model = Cuisine
        fields = ('cuisine',)


class CookingTimeForm(forms.ModelForm):
    hours = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'hours_css'}))
    minutes = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'minutes_css'}))

    class Meta:
        model = CookingTime
        fields = ('hours', 'minutes')


