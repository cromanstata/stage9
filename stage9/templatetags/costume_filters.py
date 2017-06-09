from unidecode import unidecode
from django import template
from slugify import slugify
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter(name='slug')
def slug(value):
    return slugify(value)


@register.filter(is_safe=True, name='js')
def js(obj):
    return mark_safe(json.dumps(obj))


