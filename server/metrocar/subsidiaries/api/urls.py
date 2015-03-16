'''
Created on 10.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from piston.resource import Resource

from handlers import *

subsidiary_handler = Resource(SubsidiaryHandler)
subsidiary_local_handler = Resource(SubsidiaryLocalHandler)

urlpatterns = patterns('',
    url(r'^$', subsidiary_handler, name='api_subsidiaries_subsidiary_handler'),
    url(r'^(?P<id>\d+)/$', subsidiary_handler, name='api_subsidiaries_subsidiary_handler'),
    url(r'^local/$', subsidiary_local_handler, name='api_subsidiaries_subsidiarylocal_handler'),
)