'''
Created on 11.12.2009

@author: xaralis
'''


from datetime import datetime

from django.http import HttpResponseBadRequest, HttpResponseServerError,\
    HttpResponseNotFound
from django.conf import settings

from metrocar.utils.log import get_logger, logging
from metrocar.cars.models import Car, Journey, CarPosition
from metrocar.user_management.models import MetrocarUser
from _mysql_exceptions import ProgrammingError
from decimal import Decimal

from adapters import get_adapter, InvalidFormatException

class CarUnitRequestHandler:
    """
    """
    def __init__(self):
        self._adapter = None
        self._request_data = None
        self._response_data = None
        self._car = None
        self._logger = get_logger()
    
    def handle_request(self, request, format=None):
#        if request.META.has_key('REMOTE_ADDR'):
#            source = request.META.get('REMOTE_ADDR')
#        else:
#            source = '?'
        response = self._handle_request(request, format)
        self._logger.info("Accepted incoming call. Data: " + response.content)
        return response
    
    def _handle_request(self, request, format=None):
        if format is None:
            return HttpResponseBadRequest('Incorrect request: no format '
                'selected')
        if request.method != 'POST':
            return HttpResponseBadRequest('Incorrect request: only POST method '
                'allowed')
        
        # resolve request adapter
        try:
            self._adapter = get_adapter(format)
        except InvalidFormatException, ex:
            raise HttpResponseBadRequest(unicode(ex))
        
        try:
            request_str = request.raw_post_data
        except IndexError:
            raise AssertionError('Incorrect request: missing request POST '
                'variable')
        
        if not request_str:
            raise ValueError('Incorrect request: missing request data')
        
        # begin processing request
        try:
            # preprocess request (parse etc.)
            self._request_data = self._adapter.preprocess_request(request_str)
            # process request_data
            self._response_data = self.process_request(self._request_data)
        except Exception, err:
            return HttpResponseServerError(repr(err))
        
        # postprocess response (convert to correct format etc.)
        try:
            response = self._adapter.postprocess_response(self._response_data)
        except Exception, err:
            return HttpResponseServerError(repr(err))
        return response
    
    def process_request(self, request_data):
        response_data = {'usages': {}, 'requirements': {}}
        
        if self._authorize(request_data['auth']['imei'],
            request_data['auth']['authorization_key']):
            if request_data['usages']:
                self._usages(request_data['usages'])
            if request_data['requirements']:
                response_data['requirements'] = self._requirements(
                    request_data['requirements'])
        else: raise AssertionError('Unauthorized access')
        
        return response_data
    
    def _authorize(self, imei, authorization_key):
        self._car = Car.objects.authenticate(imei, authorization_key)
        if self._car:
            self._car.update_comm_status()
            return True
        else:
            return False
    
    def _usages(self, usages):
        assert isinstance(self._car, Car)
        for usage in usages:
            user = None
            journey = None
            
            try:
                user = MetrocarUser.objects.get(pk__exact=int(usage['user_id']))
            except Exception, err:
                self._logger.log(logging.ERROR, 'Cannot fetch user: %s' % str(err))
                raise ProgrammingError('Cannot fetch user: %s' % str(err))
            
            # we have since record, start the journey
            if usage.has_key('since'):
                journey = Journey.objects.start_journey(self._car, user, 
                    usage['since'])
                
            # we have till record, finish the journey
            if usage.has_key('till'):
                journey = self._car.get_current_journey()
                if journey is None:
                    raise AssertionError('No active journey has been found')
                journey.finish(usage['till'])
                if journey.reservation is not None and journey.reservation.ready_to_finish():
                    journey.reservation.finish(usage['till'])
                    
            if journey is not None:
                # record sent positions
                from django.contrib.gis.geos import Point
                base_pos = Point(usage['base_position']['latitude'], 
                    usage['base_position']['longitude'])
                pos_count = len(usage['incremental_positions'])
                for index, pos in enumerate(usage['incremental_positions']):
                    p = Point(base_pos.x + pos['latitude'],
                        base_pos.y + pos['longitude'])
                    car_position = CarPosition(position=p, journey=journey)
                    """
                    We avoid car position change except for last update,
                    which saves a lot of time (especially because of reverse
                    address resolving)
                    """
                    if index == pos_count - 1:
                        car_position.save()
                    else:
                        car_position.save(no_pos_update=True)
                # finally add length
                journey.length += Decimal(usage['length'])
                journey.save()
            else:
                raise AssertionError('No journey has been found')
    
    def _requirements(self, requirements):
        output = {}
        for req in requirements:
            if req == 'SETTINGS':
                from metrocar.utils.models import SiteSettings
                try:
                    output['settings'] = SiteSettings.objects.get_current().get_unit_settings_dict()
                except SiteSettings.DoesNotExist:
                    pass
            elif req == 'RESERVATIONS':
                allowed_users = self._car.get_allowed_users()
                output['reservations'] = []
                for user, allowed_times in allowed_users.items():
                    phone_numbers = []
                    if user.primary_phone:
                        phone_numbers.append(user.primary_phone)
                    if user.secondary_phone:
                        phone_numbers.append(user.secondary_phone)
                    output['reservations'].append({
                        'user_id': user.pk,
                        'rfid_codes': [ user.user_card.code ],
                        'phone_numbers': phone_numbers,
                        'allowed_times': allowed_times 
                    })
        return output
    
request_handler = CarUnitRequestHandler()
