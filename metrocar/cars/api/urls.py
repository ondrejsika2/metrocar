'''
Created on 10.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *

from piston.resource import Resource

from handlers import *

car_type_handler = Resource(CarTypeHandler)
car_model_handler = Resource(CarModelHandler)
car_handler = Resource(CarHandler)
reservation_handler = Resource(ReservationHandler)
car_position_handler = Resource(CarPositionHandler)

urlpatterns = patterns('',
    # car types
    url(r'^types/$', car_type_handler, name='api_cars_cartype_handler'),
    url(r'^types/(?P<id>\d+)/$', car_type_handler, name='api_cars_cartype_handler'),
    
    # car models
    url(r'^models/$', car_model_handler, name='api_cars_carmodel_handler'),
    url(r'^models/(?P<id>\d+)/$', car_model_handler, name='api_cars_carmodel_handler'),
    
    # cars
    url(r'^$', car_handler, name='api_cars_car_handler'),
    url(r'^(?P<id>\d+)/$', car_handler, name='api_cars_car_handler'),
    url(r'^(?P<id>\d+)/reservations/$', reservation_handler, name='api_cars_reservation_handler'),
    url(r'^positions/$', car_position_handler, name='api_cars_car_position_handler'),
    url(r'^positions/(?P<geometry_format>[a-z]+)/$', car_position_handler, name='api_cars_car_position_handler'),
)