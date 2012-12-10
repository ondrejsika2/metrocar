from datetime import datetime
from pipetools import pipe, X, foreach

import geotrack

from metrocar.car_unit_api.models import CarUnit
from metrocar.car_unit_api.utils import authenticate
from metrocar.car_unit_api.validation import valid_timestamp, valid_location, valid_user_id
from metrocar.reservations.models import Reservation
from metrocar.utils.apis import APICall, parse_json, process_request, validate_request
from metrocar.utils.validation import required, optional, validate_each, valid_int, valid_string, valid_float


class StoreLog(APICall):
    """
    An API method to store one or more log-entries from a car unit.
    """

    rules = (
        required('unit_id', valid_int),
        required('entries'),
        X['entries'] | validate_each(
            required('timestamp', valid_timestamp),
            required('location', valid_location),
            optional('event', valid_string),
            optional('user_id', valid_user_id),
            optional('odometer', valid_float),
        ),
    )

    @process_request(pipe
        | parse_json
        | authenticate
        | (validate_request, rules))
    def post(self, request, data):

        for entry in data['entries']:
            geotrack.api.store(unit_id=data['unit_id'], **entry)

        return {'status': 'ok'}


class Reservations(APICall):
    """
    An API method that returns upcoming reservations for the unit making the
    request.
    """

    @process_request(pipe | parse_json | authenticate)
    def get(self, request, data):
        return {
            'status': 'ok',
            'timestamp': datetime.now(),
            'reservations': get_upcoming_reservations(data['unit_id']),
        }


def get_upcoming_reservations(unit_id):
    return (CarUnit.objects.get(unit_id=unit_id).car_id > pipe
         | Reservation.objects.get_upcoming
         | foreach(reservation_data_for_car_unit)
         | tuple)


def reservation_data_for_car_unit(reservation):
    user = reservation.user
    return {
        'user': reservation_user_data(user),
        'start': reservation.reserved_from,
        'end': reservation.reserved_until,
    }


def reservation_user_data(user):
    return {
        'id': user.id,
        'password': user.password,
    }
