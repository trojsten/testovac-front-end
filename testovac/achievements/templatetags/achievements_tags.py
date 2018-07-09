from django.template import Library

register = Library()

@register.filter
def is_in(value,arg):
    return value in arg

@register.filter('badge_count')
def _badge_count(user_or_qs):
    return badge_count(user_or_qs)

@register.filter
def number_awarded(badge, user_or_qs=None):
    return badge.number_awarded(user_or_qs)
 
