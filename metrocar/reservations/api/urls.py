# #TODO-Vojta remove this file
#
# '''
# Created on 27.3.2010
#
# @author: xaralis
# '''
#
# from django.conf.urls.defaults import *
#
# from piston.resource import Resource
#
# from metrocar.api.auth import get_authentication_handler
#
# from handlers import *
#
# reservation_handler = Resource(ReservationHandler, authentication=get_authentication_handler())
#
# urlpatterns = patterns('',
#     # pricelists
#     url(r'^$', reservation_handler, name='api_reservation_handler'),
#     url(r'^(?P<id>\d+)/$', reservation_handler, name='api_reservation_handler'),
# )