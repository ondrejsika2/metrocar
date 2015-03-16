'''
Created on 27.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from piston.resource import Resource

from handlers import *

pricelist_handler = Resource(PricelistHandler)

urlpatterns = patterns('',
    # pricelists
    url(r'^$', pricelist_handler, name='api_pricelist_handler'),
    url(r'^(?P<id>\d+)/$', pricelist_handler, name='api_pricelist_handler'),
)