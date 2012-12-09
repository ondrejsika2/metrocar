from pipetools import pipe, X

import geotrack

from metrocar.car_unit_api.utils import authenticate
from metrocar.utils.apis import APICall, parse_json, process_request, validate_request
from metrocar.utils.validation import required, optional, validate_each, valid_int, valid_string, valid_location, valid_timestamp


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
            # TODO:
            # optional('user_id', valid_user_id),
            # optional('odometer', valid_float),
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
