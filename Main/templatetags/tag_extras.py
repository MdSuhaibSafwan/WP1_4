from django import template
from EnergyCapture.models import Station

register = template.Library()

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.simple_tag
def stations(request):
    return Station.objects.all()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)