from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import (
    GenericForeignKey)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist



class Comment(models.Model):
    """ Represents an instance of Comment """

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, null=True, blank=True)
    rating = models.DecimalField("Rating", blank=True, null=True, default=None,
                                 max_digits=2, decimal_places=1,
                                 validators=[MaxValueValidator(5), MinValueValidator(0)])

    comment = models.CharField(max_length=512)
    likes_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')

    class Meta:
        ordering = ['created_at']


class Like(models.Model):
    """
    Represents an instance of a Like
    belonging to a Comment
    """
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
