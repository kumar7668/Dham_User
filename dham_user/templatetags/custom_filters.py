# custom_filters.py
from django import template
import math

register = template.Library()

@register.filter
def get_attr(value, attr_name):
    return getattr(value, attr_name, None)


@register.filter
def add_class_to_p_tag(value):
    return value.replace('<p>', '<p class="blog-text">')

@register.simple_tag
def generate_stars(rating):
    filled_stars = range(int(rating))  # Create filled stars based on the rating
    empty_stars = range(5 - int(rating))  # Create empty stars to fill up to 5
    return filled_stars, empty_stars
