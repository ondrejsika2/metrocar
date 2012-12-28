from datetime import datetime
from pipetools import pipe, unless, where, KEY, X, foreach, sort_by, first_of

from metrocar.car_unit_api.models import CarUnit
from metrocar.cars.models import Car
from metrocar.utils.apis import InvalidRequest
from metrocar.utils.validation import valid_int, valid_string
from metrocar.utils.validation import validate, required

import geotrack
from geotrack.utils import extract_timestamp


def authenticate(data):
    """
    Checks for a valid combination of ``unit_id`` and ``secret_key`` values in
    `data`.

    Also removes the ``secret_key`` for enhanced security.
    """
    invalid = pipe | 'Authentication failed ({0}).' | InvalidRequest

    valid, error = validate(
        required('unit_id', valid_int),
        required('secret_key', valid_string),
    )(data)

    if not valid:
        raise invalid(error)

    unit = unless(CarUnit.DoesNotExist, CarUnit.objects.get)(
        unit_id=data['unit_id'],
        secret_key=data['secret_key'],
    )

    if not unit:
        raise invalid('wrong "unit_id" and/or "secret_key"')

    if not unit.enabled:
        raise invalid('unit is disabled')

    return data.iteritems() > where(KEY != 'secret_key') | dict


def get_current_car_position_data(in_polygon=None):
    """
    Returns a sequence of {location, Car, timestamp} mappings.
    """
    geotrack_data = geotrack.api.query('last_position', in_polygon=in_polygon)
    return _current_position_data(geotrack_data)


def _current_position_data(geotrack_data):
    """
    Add Cars to geotrack_data for current car positions.
    """
    unit_data = geotrack_data.items()
    unit_ids = geotrack_data.keys()
    units = CarUnit.objects.filter(unit_id__in=unit_ids).select_related('car')
    unit_dict = units > foreach([X.unit_id, X]) | dict
    for unit_id, data in unit_data:
        yield {
            'location': data['location'],
            'timestamp': data['timestamp'],
            'car': unit_dict[unit_id].car,
        }


def with_parsed_timestamp(entry):
    return (entry if isinstance(entry['timestamp'], datetime)
        else dict(entry, timestamp=extract_timestamp(entry['timestamp'])))


def update_car_status(unit_id, entries):
    """
    Updates Car model from `entries` received through the API.
    """
    car = CarUnit.objects.get(unit_id=unit_id).car
    car and (entries > pipe
        | foreach(with_parsed_timestamp)
        | sort_by(X['timestamp'])
        | first_of
        | (update_car, car))


def update_car(car, entry):
    if not car.last_echo or (car.last_echo < entry['timestamp']):
        Car.objects.filter(id=car.id).update(
            last_echo=entry['timestamp'],
            _last_position='POINT ({0} {1})'.format(*entry['location']),
            _last_address=None,
        )
