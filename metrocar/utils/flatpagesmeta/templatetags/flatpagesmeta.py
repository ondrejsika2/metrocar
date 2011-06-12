from django import template
from django.contrib.flatpages.models import FlatPage

from metrocar.utils.flatpagesmeta.models import *

register = template.Library()

@register.tag
def meta_keywords(parser, token):
    tag_name, flatpage_id = token.split_contents()
    return MetaKeywordsObject(flatpage_id)

class MetaKeywordsObject(template.Node):
    def __init__(self, flatpage_id):
        self.flatpage_id = template.Variable(flatpage_id)
        
    def render(self, context):
        try:
            return Meta.objects.filter(flatpage = self.flatpage_id.resolve(context))[0].keywords
        except:
            return ''

@register.tag
def meta_description(parser, token):
    tag_name, flatpage_id = token.split_contents()
    return MetaDescriptionObject(flatpage_id)

class MetaDescriptionObject(template.Node):
    def __init__(self, flatpage_id):
        self.flatpage_id = template.Variable(flatpage_id)
    def render(self, context):
        try:
            return Meta.objects.filter(flatpage = self.flatpage_id.resolve(context))[0].description
        except:
            return ''