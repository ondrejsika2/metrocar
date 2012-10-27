from functools import wraps
from pipetools import pipe, unless, where, KEY

from django.utils import simplejson as json

from metrocar.car_unit_api.models import CarUnit
from metrocar.car_unit_api.validation import valid_int, valid_string
from metrocar.car_unit_api.validation import validate, required
from metrocar.utils.views import JsonResponse


class InvalidRequest(Exception):
    "An exception that is risen on an invalid API request from a client. "


def process_request(process):
    """
    Decorator to process an incoming request using the supplied `process`
    function.

    The `process` function is supposed to take the request object and any URL
    parameters if present and either:

    *   return a value -- presumably cleaned data for the decorated method

    *   or raise an ``InvalidRequest`` exception with a message explaining
        what was wrong with the request, which will be directly returned to
        the client.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(view, request, *args, **kwargs):
            try:
                clean_data = process(request, *args, **kwargs)
            except InvalidRequest, e:
                return JsonResponse({
                    'status': 'error',
                    'message': unicode(e),
                }, status=400)
            return view_func(view, request, clean_data)
        return wrapped
    return decorator


def parse_json(request):
    """
    Parse raw JSON data from a request.
    """
    raw_data = request.body
    if not raw_data:
        raise InvalidRequest('Missing JSON data.')
    try:
        return json.loads(request.body)
    except ValueError, ex:
        raise InvalidRequest('Invalid JSON (%s).' % ex)


def validate_request(rules, data):
    valid, error = validate(rules)(data)
    if not valid:
        raise InvalidRequest(error)
    return data


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
