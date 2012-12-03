from pipetools import pipe, unless, where, KEY

from metrocar.utils.apis import InvalidRequest
from metrocar.car_unit_api.models import CarUnit
from metrocar.car_unit_api.validation import valid_int, valid_string
from metrocar.car_unit_api.validation import validate, required


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
