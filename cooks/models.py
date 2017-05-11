from django.db import models
from . import fields
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

class Recipe(models.Model):
    title = models.CharField("Title", blank=True, null=True, max_length=200, unique=True)
    photo = models.ImageField(upload_to="media/cooks/img", blank=True, null=True)
    summary = models.TextField("Summary", blank=True, null=True)
    description = models.TextField("Description", blank=True, null=True)
    portions = models.IntegerField("Portions", blank=True, null=True)
    publish_date = models.DateTimeField("publish_date")

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


class IngredientSearch(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient']


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

# Create your models here.
