'''
Created on 10.3.2010

@author: xaralis
'''

from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc

from metrocar.cars.models import *
from metrocar.reservations.models import Reservation
    
class CarTypeHandler(BaseHandler):
    """
    Interface for querying car types in our database.
    
    Supports only GET request - read only.
    """
    
    allowed_methods = ('GET',)
    model = CarType
    fields = ('type', ('models', ('full_name', 'resource_uri',)))
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_cars_cartype_handler', ['id'])

class CarModelHandler(BaseHandler):
    """
    Interface for querying car models in our database.
    
    Supports only GET request - read only.
    """
    
    allowed_methods = ('GET',)
    model = CarModel
    fields = (
        'name', 
        ('manufacturer', ('name',)),
        'full_name', 
        ('type', ('type', 'resource_uri')), 
        'engine', 
        'seats_count', 
        'storage_capacity', 
        ('main_fuel', ('title',)), 
        ('alternative_fuel', ('title')), 
        'notes',
        ('cars', ('registration_number', 'resource_uri'))
    )
    
    @classmethod
    def full_name(cls, model):
        """
        Proxy to unicode method of model.
        """
        return unicode(model)
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_cars_carmodel_handler', ['id'])

class CarHandler(BaseHandler):
    """
    Interface for querying cars.
    
    Offers several ways to simplify geolocation of our cars. Supports only 
    GET request - read only.
    """
    
    allowed_methods = ('GET',)
    model = Car
    fields = (
        'id',
        'imei',
        'full_name',
        'registration_number',
        ('model', (('type', ('type', 'resource_uri')), 'resource_uri')),
        ('color', ('color',)),
        'last_position',
        'last_address',
        'last_echo'
        'active',
        'dedicated_parking_only',
        ('home_subsidiary', ('resource_uri'))
    )
    exclude = ()
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_cars_car_handler', ['id'])
    
class ReservationHandler(BaseHandler):
    """
    Used to list cars reservations.
    
    Supports only GET request - read only.
    """
    
    allowed_methods = ('GET',)
    model = Reservation
    fields = (
        'reserved_from',
        'reserved_until',
        ('user', ('username', 'resource_uri'))
    )
    
    def read(self, request, id):
        """
        Reads all pending reservations for car of given 'id'.
        """
        try:
            car = Car.objects.get(pk=id)
        except:
            return rc.NOT_FOUND
        return car.reservations.pending()
    
class CarPositionHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = (
        'full_name',
        'last_position',
        'last_address',
        'resource_uri',
    )
    
    def read(self, request, geometry_format='geojson'):
        """
        Returns summary of all cars which belong to this subsidiary and 
        submits their positions.
        """
        return Car.objects.all()
