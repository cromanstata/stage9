from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth.models import User
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

