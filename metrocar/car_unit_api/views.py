from datetime import datetime
from pipetools import pipe, X, foreach

import geotrack

from metrocar.car_unit_api.models import CarUnit
from metrocar.car_unit_api.utils import authenticate, update_car_status
from metrocar.car_unit_api.validation import valid_timestamp, valid_user_id
from metrocar.reservations.models import Reservation
from metrocar.utils.apis import APICall, parse_json, process_request, validate_request
from metrocar.utils.geo.validation import valid_location
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
            optional('velocity', valid_float),
            optional('consumption', valid_float),
            optional('fuel_remaining', valid_float),
            optional('altitude', valid_float),
            optional('engine_temp', valid_float),
            optional('engine_rpm', valid_float),
            optional('throttle', valid_float),
            optional('gps_accuracy', valid_float),
        ),
    )

    @process_request(pipe
        | parse_json
        | authenticate
        | (validate_request, rules))
    def post(self, request, data):
        store(data['unit_id'], data['entries'])
        return {'status': 'ok'}


def store(unit_id, entries):
    """
    The actual storing action. Assumes valid data.
    """
    for entry in entries:
        geotrack.api.store(unit_id=unit_id, **entry)

    update_car_status(unit_id, entries)


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
        'reservationId' : reservation.id,
    }


def reservation_user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'password': user.password,
    }
