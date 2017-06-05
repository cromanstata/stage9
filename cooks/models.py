from django.db import models
from . import fields
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.contrib.contenttypes.fields import GenericRelation
from cooks.exceptions import AlreadyExistsError
from comments.models import Comment
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from slugify import slugify

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

from cooks.signals import (
    favorite_created, favorite_removed,
    favorer_created, favorer_removed, favorite_recipe_created, favorite_recipe_removed,
    like_created, like_removed, like_recipe_created, like_recipe_removed,
    rating_created, rating_removed, rating_recipe_created, rating_recipe_removed
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
    title = models.CharField("Title", max_length=200, unique=True)
    photo = models.ImageField(upload_to="media/cooks/img", blank=True, null=True)
    summary = models.TextField("Summary", max_length=400, blank=True, null=True)
    description = models.TextField("Description", max_length=2000, blank=True, null=True)
    portions = models.IntegerField("Portions", blank=True, null=True)
    publish_date = models.DateTimeField("publish_date")
    comments = GenericRelation(Comment)
    author = models.ForeignKey(User, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    search_fields = ("title", "summary", "description",)

    def __str__(self):
        if self.title == None:
            return ''
        else:
            return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Recipe, self).save(*args, **kwargs)

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
    slug = models.SlugField(blank=True, null=True)

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
        if self.note:
           _ingredient = '%s - %s' % (_ingredient, self.note)

        return _ingredient

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.ingredient)

        super(Ingredient, self).save(*args, **kwargs)

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
        return self.mealtype

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


class WorkingTime(models.Model):
    """
    Provides working hour fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="working_hours")
    hours = models.IntegerField(_("hours"), default=0)
    minutes = models.IntegerField(_("minutes"), default=0)

    def __unicode__(self):
        return "%02d:%02d" %(self.hours, self.minutes)

    class Meta:
        verbose_name = _("working hour")
        verbose_name_plural = verbose_name


class CookingTime(models.Model):
    """
    Provides cooking time fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="cooking_time")
    hours = models.IntegerField(_("hours"), blank=True, null=True, default=0)
    minutes = models.IntegerField(_("minutes"), blank=True, null=True, default=0)

    def __unicode__(self):
        return "%02d:%02d" %(self.hours, self.minutes)

    def __str__(self):
        if self.hours and self.minutes:
            return "%02d:%02d" %(self.hours, self.minutes)
        if self.minutes:
            return "%02d:%02d" %(0, self.minutes)
        if self.hours:
            return "%02d:%02d" %(self.hours, 0)
        else:
            return "%02d:%02d" % (0, 0)

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

    def num_favorers(self, recipe):
        """ Return a list of all users who favour the given recipe """
        # key = cache_key('following', user.pk)
        # following = cache.get(key)

        # if following is None:
        qs = Favorite.objects.filter(recipe=recipe).all()
        count = qs.__len__()

        if count:
            return count
        else:
            count == 0
            return count

    def add_favorite(self, favorer, recipe):
        """ Create 'favorer' favorites 'recipe' relationship """
        relation, created = Favorite.objects.get_or_create(favorer=favorer, recipe=recipe)

        if created is False:
            raise AlreadyExistsError("User '%s' already favors '%s'" % (favorer, recipe))

        favorite_created.send(sender=self, favorer=favorer)
        favorer_created.send(sender=self, recipe=recipe)
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

    def add_like(self, liker, recipe):
        """ Create a like for a spesific user """
        like, created = Like.objects.get_or_create(liker=liker, recipe=recipe)

        if created is False:
            raise AlreadyExistsError("User '%s' already likes '%s'" % (liker, recipe))

        like_created.send(sender=self, liker=liker)
        like_recipe_created.send(sender=self, recipe=recipe)

        return like

    def remove_like(self, liker, recipe):
        """ Removes like of a spesific user """
        try:
            rel = Like.objects.get(liker=liker, recipe=recipe)
            like_removed.send(sender=rel, liker=rel.liker)
            like_recipe_removed.send(sender=rel, recipe=recipe)
            rel.delete()
            return True
        except Like.DoesNotExist:
            return False

    def likes(self, liker, recipe):
        """ Does user faorites recipe? Smartly uses caches if exists """
        try:
            Like.objects.get(liker=liker, recipe=recipe)
            return True
        except Like.DoesNotExist:
            return False

    def get_likes(self, recipe):
        #number of likes for the recipe
        try:
            likes = Like.objects.filter(recipe=recipe)
            like_count = likes.count()
            print (like_count)
            return (like_count)

        except ObjectDoesNotExist:
            #recipe = Recipe.objects.get(id=recipe)
            #likes = Like(recipe=recipe, likes_count=0, updated=timezone.now())
            #likes.save()
            #return likes
            print ("no counts for this recipe")
            like_count = 0
            return like_count

class Like(models.Model):
    """
    Count likes for a recipe
    Need to add users later?
    """
    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"), related_name="like" ,on_delete=models.CASCADE)
    liker = models.ForeignKey(AUTH_USER_MODEL, related_name="liking", on_delete=models.CASCADE)
    updated = models.DateTimeField(default=timezone.now)

    # all methods for getting info on this class
    objects = LikesManager()

    class Meta:
        verbose_name = _('Likes')
        verbose_name_plural = verbose_name

    #def __str__(self):
        #return str(self.likes)
    #def __int__(self):
        #return self.likes
    def __str__(self):
        return "User #%s likes #%s" % (self.liker_id, self.recipe_id)


class RatingManager(models.Manager):
    """ Rating manager """

    def add_rating(self, rater, recipe, rating):
        """ Create a like for a spesific user """
        rating, created = Rating.objects.get_or_create(rater=rater, recipe=recipe, rating=rating)

        if created is False:
            raise AlreadyExistsError("User '%s' already rated '%s' with '%s'" % (rater, recipe, rating))

        rating_created.send(sender=self, rater=rater)
        rating_recipe_created.send(sender=self, recipe=recipe, rating=rating)

        return rating

    def remove_rating(self, rater, recipe):
        """ Removes rating of a spesific user """
        try:
            rel = Rating.objects.get(rater=rater, recipe=recipe)
            rating_removed.send(sender=rel, rater=rel.rater)
            rating_recipe_removed.send(sender=rel, recipe=recipe)
            rel.delete()
            return True
        except Rating.DoesNotExist:
            return False

    def rated(self, rater, recipe):
        """ Did user rate the recipe? Smartly uses caches if exists """
        try:
            Rating.objects.get(rater=rater, recipe=recipe)
            return True
        except Like.DoesNotExist:
            return False

    def get_rating(self, recipe):
        #number of likes for the recipe
        try:
            ratings = Rating.objects.filter(recipe=recipe)
            rating_count = 0
            rating_sum = 0
            for rating in ratings:
                rating_sum += rating.rating
                rating_count += 1
            return round(rating_sum/rating_count * 2) / 2

        except ObjectDoesNotExist:
            #recipe = Recipe.objects.get(id=recipe)
            #likes = Like(recipe=recipe, likes_count=0, updated=timezone.now())
            #likes.save()
            #return likes
            print ("no ratings for this recipe")
            rating_avg = 0
            return rating_avg

class Rating(models.Model):
    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"), related_name="rating", on_delete=models.CASCADE)
    rating = models.DecimalField("Rating", blank=True, null=True,
                                 max_digits=2, decimal_places=1,
                                 validators=[MaxValueValidator(5), MinValueValidator(0)])
    rater = models.ForeignKey(AUTH_USER_MODEL, related_name="rater", on_delete=models.CASCADE)
    updated = models.DateTimeField(default=timezone.now)
    comment_key = models.ForeignKey("comments.Comment", verbose_name=_("Comment"), related_name="rating4cooks", on_delete=models.CASCADE)

    # all methods for getting info on this class
    objects = RatingManager()

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = verbose_name

    def __str__(self):
        return "User #%s rates #%s recipe #%s " % (self.rater_id, self.rating, self.recipe_id)
# Create your models here.
