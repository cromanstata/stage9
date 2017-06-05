from django import forms
from .models import Comment
from cooks.models import Rating
from django.forms.models import inlineformset_factory


class CommentForm(forms.ModelForm):

    """Author: Aly Yakan"""
    comment = forms.CharField(widget=forms.Textarea(attrs = {'placeholder': "Write a review or leave a comment..."}))
    rating = forms.DecimalField(required=False, widget=forms
                                .HiddenInput(attrs={}))
                                #.NumberInput(attrs={'step': 0.5}))

    class Meta:
        model = Comment
        exclude = ('likes_count', 'dislikes_count', 'content_type', 'object_id',
                   'content_object')


"""
class RatingForm(forms.ModelForm):
    rating = forms.DecimalField(widget=forms.NumberInput(attrs = {'step': 0.5}))

    class Meta:
        model = Rating
        exclude = ('updated', 'rater_id', 'recipe_id')
"""