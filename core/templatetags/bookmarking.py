import datetime
from django import template
# from ..models import GeneralLink

register = template.Library()

# @register.filter(name='cut')
def cutting(value, index):
    """Removes all values of arg from the given string"""
    return value[:index]


# filter
# {{ link_list|cut:10 }}   -> cut(link_list, 10)


def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

# filter
# {{link.name|lower}}   -> lower(link.name) 

register.filter('cut', cutting)
register.filter('mylower', lower)


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def cut_queryset(queryset, count):
    return queryset[:count]

# <p>{%  current_time 'YYYY-MM-DD' %}</p>  -> <p>2022-05-13</p>

# {% cut_queryset link_list 10 as link_list_2 %}

#  {% for link link_list_2 %}  

@register.simple_tag
def is_bookmarked(link, user, status):
    if not user.is_authenticated:
        return False
    return link.bookmarkedlink_set.filter(user=user, status=status).exists()


# {% is_bookmarked link request.user 'L' %}