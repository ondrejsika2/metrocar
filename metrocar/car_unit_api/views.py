from pipetools import pipe, X

from django.http import HttpResponse
from django.views.generic.base import View

import geotrack

from metrocar.car_unit_api.utils import parse_json, authenticate
from metrocar.car_unit_api.utils import process_request, validate_request
from metrocar.car_unit_api.validation import required, optional, validate_each
from metrocar.car_unit_api.validation import valid_int, valid_string
from metrocar.car_unit_api.validation import valid_location, valid_timestamp
from metrocar.utils.views import JsonResponse


class APICall(View):
    """
    Base for an API view. Automatically converts responses that are not already
    an instance of an HttpResponse to JSON-responses.
    """
    def dispatch(self, request, *args, **kwargs):
        response = super(APICall, self).dispatch(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        return JsonResponse(response)


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
