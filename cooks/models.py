from django.db import models
from . import fields
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.contrib.contenttypes.fields import GenericRelation
from cooks.exceptions import AlreadyExistsError
from comments.models import Comment
from django.conf import settings
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ObjectDoesNotExist

from cooks.signals import (
    favorite_created, favorite_removed,
    favorer_created, favorer_removed, favorite_recipe_created, favorite_recipe_removed
)

CACHE_TYPES = {
    'favorites': 'fav-%s',
}

BUST_CACHES = {
    'favorites': ['favorites'],
}

def cache_key(type, user_pk):
    """
    Build the cache key for a particular type of cached value
    """
    return CACHE_TYPES[type] % user_pk


def bust_cache(type, user_pk):
    """
    Bust our cache for a given type, can bust multiple caches
    """
    bust_keys = BUST_CACHES[type]
    keys = [CACHE_TYPES[k] % user_pk for k in bust_keys]
    cache.delete_many(keys)


class Recipe(models.Model):
    title = models.CharField("Title", blank=True, null=True, max_length=200, unique=True)
    photo = models.ImageField(upload_to="media/cooks/img", blank=True, null=True)
    summary = models.TextField("Summary", blank=True, null=True)
    description = models.TextField("Description", blank=True, null=True)
    portions = models.IntegerField("Portions", blank=True, null=True)
    publish_date = models.DateTimeField("publish_date")
    comments = GenericRelation(Comment)
    author = models.ForeignKey(User, null=True, blank=True)

    search_fields = ("title", "summary", "description",)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ("publish_date",)


class Ingredient(models.Model):
    """
    Provides ingredient fields for managing recipe content and making
    it searchable.
    """
    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"), related_name="ingredients", on_delete=models.CASCADE)
    quantity = models.CharField(_("Quantity"), max_length=10, blank=True, null=True)
    unit = models.CharField(_("Unit"), choices=fields.UNITS, blank=True, null=True, max_length=20)
    ingredient = models.CharField(_("Ingredient"), max_length=100)
    note = models.CharField(_("Note"), max_length=200, blank=True, null=True)

    #tring out django-taggit

    def __str__(self):
        _ingredient = '%s' % self.ingredient

        if self.unit:
            _ingredient = '%s %s' % (self.get_unit_display(), _ingredient)

        #for python anywhere should work:
        #if self.unit:
         #   if 'NoneType' in self.request.GET:
          #      _ingredient = '%s %s' % (None,_ingredient)
           # else:
            #    _ingredient = '%s %s' % (self.get_unit_display(), _ingredient)

        if self.quantity:
            _ingredient = '%s %s' % (self.quantity, _ingredient)
        #python anywhere doesnt register len for somereason so should be changed
        if len(self.note):
           _ingredient = '%s - %s' % (_ingredient, self.note)

        return _ingredient

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")


class Difficulty (models.Model):
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="difficulty",
                                  on_delete=models.CASCADE)
    difficulty = models.CharField(_("Difficulty"), choices=fields.DIFFICULTIES, blank=True, null=True, max_length=20)

    def __str__(self):
        return self.difficulty

    class Meta:
        verbose_name = _("Difficulty")


class MealType (models.Model):
    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"), related_name="meal_type", on_delete=models.CASCADE)
    mealtype = models.CharField(_("Meal type"), choices = fields.MEALTYPE, blank=True, null=True, max_length = 50)

    def __str__(self):
        _mealtype = '%s' % self.mealtype
        return _mealtype

    class Meta:
        verbose_name = _("Mealtype")
        verbose_name_plural = _("Mealtypes")


class Cuisine (models.Model):
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="cuisine", on_delete=models.CASCADE)
    cuisine = models.CharField(_("Cuisine"), choices=fields.CUISINE, blank=True, null=True, max_length=50)

    def __str__(self):
        return self.cuisine

    class Meta:
        verbose_name = _("Cuisine")
        verbose_name_plural = verbose_name


class Period(models.Model):
    """
    Provides fields for a period of time
    """
    hours = models.IntegerField(_("hours"), default=0)
    minutes = models.IntegerField(_("minutes"), default=0)

    def __unicode__(self):
        return "%02d:%02d" %(self.hours, self.minutes)

    class Meta:
        abstract = True


class WorkingTime(Period):
    """
    Provides working hour fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="working_hours")

    class Meta:
        verbose_name = _("working hour")
        verbose_name_plural = verbose_name


class CookingTime(Period):
    """
    Provides cooking time fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="cooking_time")

    class Meta:
        verbose_name = _("cooking time")
        verbose_name_plural = verbose_name


class FavoriteManager(models.Manager):
    """ Favorites manager """

    def favorites(self, user):
        """ Return a list of all favorite recipes """
        #maybe will add cache buster later?

        #key = cache_key('followers', user.pk)
        #followers = cache.get(key)

        qs = Favorite.objects.filter(favorer=user).all()
        favorites = [u.recipe for u in qs]

        return favorites

    def favorers(self, recipe):
        """ Return a list of all users who favour the given recipe """
        #key = cache_key('following', user.pk)
        #following = cache.get(key)

        #if following is None:
        qs = Favorite.objects.filter(recipe=recipe).all()
        favorers = [u.favorer for u in qs]
        #cache.set(key, following)

        return favorers

    def add_favorite(self, favorer, recipe):
        """ Create 'favorer' favorites 'recipe' relationship """
        relation, created = Favorite.objects.get_or_create(favorer=favorer, recipe=recipe)

        if created is False:
            raise AlreadyExistsError("User '%s' already favors '%s'" % (favorer, recipe))

        favorite_created.send(sender=self, favorer=favorer)
        favorer_created.send(sender=self, recipee=recipe)
        favorite_recipe_created.send(sender=self, favorers=relation)

        return relation

    def remove_favorite(self, favorer, recipe):
        """ Remove 'favorer' favorites 'recipe' relationship """
        try:
            rel = Favorite.objects.get(favorer=favorer, recipe=recipe)
            favorite_removed.send(sender=rel, favorer=rel.favorer)
            favorer_removed.send(sender=rel, recipee=rel.recipe)
            favorite_recipe_removed.send(sender=rel, favorers=rel)
            rel.delete()
            return True
        except Favorite.DoesNotExist:
            return False

    def favors(self, favorer, recipe):
        """ Does user faorites recipe? Smartly uses caches if exists """
        try:
            Favorite.objects.get(favorer=favorer, recipe=recipe)
            return True
        except Favorite.DoesNotExist:
            return False


class Favorite (models.Model):
    """
    Addes users who favorite this recipe
    """
    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"), related_name="favorite", on_delete=models.CASCADE)
    favorer = models.ForeignKey(AUTH_USER_MODEL, related_name='favoring', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    #all methods for getting info on this class
    objects = FavoriteManager()

    class Meta:
        verbose_name = _('Favorite Recipe')
        verbose_name_plural = _('Fvorite Recipes')
        unique_together = ('recipe', 'favorer')

    def __str__(self):
        return "User #%s favorites #%s" % (self.favorer_id, self.recipe_id)


class LikesManager(models.Manager):
    """ Favorites manager """

    def add_like(self, recipe):
        """ ADD LIKE """
        likes = Like.objects.get(recipe=recipe)
        setattr(likes, 'likes_count', likes.likes_count + 1)
        likes.save()

        #signals i might add:
        #Recipe_liked.send(sender=self, favorer=favorer)
        #favorer_created.send(sender=self, recipee=recipe)
        #favorite_recipe_created.send(sender=self, favorers=relation)

    def remove_like(self, recipe):
        """ REMOVE LIKE """
        likes = Like.objects.get(recipe=recipe)
        setattr(likes, 'likes_count', likes.likes_count - 1)
        likes.save()

    def get_likes(self, recipe):
        #number of likes for the recipe
        try:
            likes = Like.objects.get(recipe=recipe)

        except ObjectDoesNotExist:
            recipe = Recipe.objects.get(id=recipe)
            likes = Like(recipe=recipe, likes_count=0, updated=timezone.now())
            likes.save()
            return likes

        return likes

class Like(models.Model):
    """
    Count likes for a recipe
    Need to add users later?
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="like" ,on_delete=models.CASCADE)
    #user = models.ForeignKey("User", verbose_name=_("User"), related_name="liker", on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    updated = models.DateTimeField(default=timezone.now)

    # all methods for getting info on this class
    objects = LikesManager()

    class Meta:
        verbose_name = _('Likes')
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.likes_count)
    def __int__(self):
        return self.likes_count
# Create your models here.
