
from djangosanetesting.cases import DatabaseTestCase

from metrocar.utils.apis import InvalidRequest
from metrocar.car_unit_api.utils import authenticate
from metrocar.car_unit_api.testing_data import unit

from test_metrocar.helpers import skipIfNotGeoEnabled


class TestAuthenticate(DatabaseTestCase):

    @skipIfNotGeoEnabled
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
