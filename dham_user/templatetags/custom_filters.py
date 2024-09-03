# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_attr(value, attr_name):
    return getattr(value, attr_name, None)



