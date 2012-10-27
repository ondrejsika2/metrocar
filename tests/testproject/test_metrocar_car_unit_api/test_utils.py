from pipetools import X

from django.utils import simplejson as json

from djangosanetesting.cases import UnitTestCase
from djangosanetesting.cases import DatabaseTestCase

from metrocar.utils import Bunch
from metrocar.car_unit_api.utils import parse_json, InvalidRequest
from metrocar.car_unit_api.utils import authenticate, validate_request
from metrocar.car_unit_api.utils import process_request
from metrocar.car_unit_api.validation import check
from metrocar.car_unit_api.testing_data import unit


class TestParseJson(UnitTestCase):

    def test_ok(self):
        request = Bunch(body='{"some": "value"}')
        self.assertEqual(parse_json(request), {'some': 'value'})

    def test_empty(self):
        request = Bunch(body='')
        with self.assertRaises(InvalidRequest) as ctx:
            parse_json(request)
        self.assertEqual(str(ctx.exception), 'Missing JSON data.')

    def test_invalid(self):
        request = Bunch(body='{12:34}')
        with self.assertRaises(InvalidRequest) as ctx:
            parse_json(request)
        self.assertEqual(str(ctx.exception),
            'Invalid JSON (Expecting property name: line 1 column 1 (char 1)).')


class TestAuthenticate(DatabaseTestCase):

    def setUp(self):
        self.secret_key = 'asdf8s6f7asdf7ad7f6a'
        self.disabled_unit_key = 'sdfafafa'
        self.unit = unit(123, secret_key=self.secret_key)
        self.disabled_unit = unit(456, secret_key=self.disabled_unit_key,
            enabled=False)

    def tearDown(self):
        self.unit.delete()

    def test_valid(self):
        data = {
            'unit_id': 123,
            'secret_key': self.secret_key,
            'other': 'data',
        }
        self.assertEqual(authenticate(data), {
            'unit_id': 123,
            'other': 'data',
        })

    def test_invalid_key(self):
        data = {
            'unit_id': 123,
            'secret_key': 'wrong',
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception),
            'Authentication failed (wrong "unit_id" and/or "secret_key").')

    def test_invalid_id(self):
        data = {
            'unit_id': 1234,
            'secret_key': self.secret_key,
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception),
            'Authentication failed (wrong "unit_id" and/or "secret_key").')

    def test_invalid_missing_key(self):
        data = {
            'unit_id': 123,
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception),
            'Authentication failed (missing "secret_key" field).')

    def test_invalid_missing_id(self):
        data = {
            'secret_key': self.secret_key,
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception),
            'Authentication failed (missing "unit_id" field).')

    def test_invalid_missing_id_and_key(self):
        data = {
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception),
            'Authentication failed (missing "unit_id" field).')

    def test_disabled_unit(self):
        data = {
            'unit_id': 456,
            'secret_key': self.disabled_unit_key,
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception),
            'Authentication failed (unit is disabled).')

    def test_invalid_unit_id_format(self):
        data = {
            'unit_id': 'asdf',
            'secret_key': self.disabled_unit_key,
            'other': 'data',
        }
        with self.assertRaises(InvalidRequest) as ctx:
            authenticate(data)
        self.assertEqual(str(ctx.exception), 'Authentication failed '
            '("unit_id" should be an integer, not "asdf").')


class TestValidateRequest(UnitTestCase):

    def setUp(self):
        self.rules = [
            check(X > 0)
        ]

    def test_valid(self):
        self.assertEqual(validate_request(self.rules, 3), 3)

    def test_invalid(self):
        with self.assertRaises(InvalidRequest):
            validate_request(self.rules, -1)


class TestProcessRequest(UnitTestCase):

    def test_valid(self):
        dummy_request = object()

        def process(request):
            self.assertEqual(request, dummy_request)
            return 'DATA'

        @process_request(process)
        def get(view, request, data):
            self.assertEqual(request, dummy_request)
            self.assertEqual(data, 'DATA')
            return 'RESULT'

        result = get(None, dummy_request)
        self.assertEqual(result, 'RESULT')

    def test_invalid(self):
        dummy_request = object()

        def process(request):
            raise InvalidRequest('ERROR MSG')

        @process_request(process)
        def get(view, request, data):
            return 'RESULT'

        result = get(None, dummy_request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(json.loads(result.content),
            {'status': 'error', 'message': 'ERROR MSG'})
