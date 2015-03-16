'''
Created on 10.3.2010

@author: xaralis
'''

from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import mark_safe

from metrocar.cars.utils import get_car_infomap, get_map_for_geometry

register = template.Library()

class CarMapOverviewNode(template.Node):
    def __init__(self, var, width, height):
        self.var = var
        self.width = width
        self.height = height
    
    def render(self, context):
        context[self.var] = get_car_infomap(self.width, self.height)
        return ''

@register.tag(name='car_map_overview')
def car_map_overview(parser, token):
    """
    Adds InfoMap with car positions to the template context.    
    Example: {% car_map_overview 100% 200px as map %}
    """
    tokens = token.split_contents()
    
    if len(tokens) < 3:
        raise TemplateSyntaxError("Number of tokens doesn't match requirements")
    var = tokens[-1]
    width = '100%'
    height = '300px'
    if len(tokens) == 5:
        width = str(tokens[1])
        height = str(tokens[2])
    
    return CarMapOverviewNode(var, width, height)
car_map_overview.is_safe = True

