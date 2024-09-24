# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_attr(value, attr_name):
    return getattr(value, attr_name, None)


@register.filter
def add_class_to_p_tag(value):
    return value.replace('<p>', '<p class="blog-text">')
