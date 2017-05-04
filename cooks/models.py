from django.db import models
from . import fields
from django.utils.translation import ugettext_lazy as _

class Recipe(models.Model):
    title = models.CharField("Title", blank=True, null=True, max_length=200)
    photo = models.ImageField(upload_to="media/cooks/img")
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

    def __str__(self):
        _ingredient = '%s' % self.ingredient

        if self.unit:
            _ingredient = '%s %s' % (self.get_unit_display(), _ingredient)

        if self.quantity:
            _ingredient = '%s %s' % (self.quantity, _ingredient)

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
        verbose_name = _("difficulty")


# Create your models here.
