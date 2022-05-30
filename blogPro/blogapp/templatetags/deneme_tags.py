from django import template
from ..models import category

register=template.Library()

@register.simple_tag
def genre_post():
    kategoriler=category.objects.all()
    return kategoriler