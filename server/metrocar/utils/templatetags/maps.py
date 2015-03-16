'''
Created on 12.3.2010

@author: xaralis
'''

from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import mark_safe

from metrocar.cars.utils import get_map_for_geometry

register = template.Library()

class MapForGeometryNode(template.Node):
    def __init__(self, var, geo, width, height):
        self.var = var
        self.geo = geo
        self.width = width
        self.height = height
    
    def render(self, context):
        geo = template.resolve_variable(self.geo, context)
        context[self.var] = get_map_for_geometry(geo, self.width, self.height)
        return ''

@register.tag(name='map_for_geometry')
def map_for_geometry(parser, token):
    " Example: {% map_for_geometry object.geometry 200 100 as map %}"
    tokens = token.split_contents()
    
    if len(tokens) < 4:
        raise TemplateSyntaxError("Number of tokens doesn't match requirements")
    geo = tokens[1]
    var = tokens[-1]
    width = '100%'
    height = '200px'
    if len(tokens) == 6:
        width = str(tokens[2])
        height = str(tokens[3])
    
    return MapForGeometryNode(var, geo, width, height)
map_for_geometry.is_safe = True