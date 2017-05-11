from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth.models import User
from cooks.models import Recipe, Ingredient, Cuisine, MealType
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['remember'].label = 'Stay signed in'
        self.fields['remember'].initial = True


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CousineForm(forms.Form):
    CUISINE = (
        ("ASIAN", _("Asian")),
        ("CARIBBEAN", _("Caribbean")),
        ("CHINESE", _("Chinese")),
        ("FRENCH", _("French")),
        ("RUSSIAN", _("Russian")),
        ("INDIAN", _("Indian")),
        ("ITALIAN", _("Italian")),
        ("MEXICAN", _("Mexican")),
        ("MEDITERRANEAN", _("Mediterranean")),
    )
    Cuisine = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CUISINE)
