'''
Created on 28.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *

from metrocar.car_unit_management.handler import request_handler 

urlpatterns = patterns('',
    # car unit management communication interface
    url(r'^(?P<format>[a-z]+)/$', request_handler.handle_request, name='metrocar_car_unit_management_handler'),
    url(r'^$', request_handler.handle_request, name='metrocar_car_unit_management_handler'),
)
