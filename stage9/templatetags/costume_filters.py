from unidecode import unidecode
from django import template
from slugify import slugify

register = template.Library()


@register.filter(name='slug')
def slug(value):
    return slugify(value)


