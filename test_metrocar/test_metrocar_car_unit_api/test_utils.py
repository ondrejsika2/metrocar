from pipetools import sort_by, X

import django.test
from metrocar.car_unit_api.models import CarUnit

from metrocar.utils.apis import InvalidRequest
from metrocar.car_unit_api.utils import authenticate, _current_position_data
from metrocar.car_unit_api.testing_data import unit
from metrocar.cars import testing_data as cars_testing_data

from test_metrocar.helpers import skipIfNotGeoEnabled


class TestAuthenticate(django.test.TestCase):

    @skipIfNotGeoEnabled
    def setUp(self):
        CarUnit.objects.all().delete()

        self.secret_key = 'asdf8s6f7asdf7ad7f6a'
        self.disabled_unit_key = 'sdfafafa'
        self.unit = unit(123, secret_key=self.secret_key)
        self.disabled_unit = unit(456, secret_key=self.disabled_unit_key, enabled=False)

    def tearDown(self):
        pass

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


class TestCurrentPositionData(django.test.TestCase):

    def test_empty(self):
        geotrack_data = {}
        self.assertEqual(tuple(_current_position_data(geotrack_data)), ())

    def test_not_empty(self):
        car1, car2 = cars_testing_data.create()['cars'][:2]
        unit1 = unit(123, car1)
        unit2 = unit(456, car2)

        geotrack_data = {
            123: {'location': 'LOC1', 'timestamp': 'TS1'},
            456: {'location': 'LOC2', 'timestamp': 'TS2'},
        }

        result = _current_position_data(geotrack_data)
        expected = (
            {'location': 'LOC1', 'timestamp': 'TS1', 'car': car1},
            {'location': 'LOC2', 'timestamp': 'TS2', 'car': car2},
        )

        self.assertEqual(
            # don't know (or care about) the output order,
            # so we have to somehow sort them
            result > sort_by(X['timestamp']) | tuple,
            expected > sort_by(X['timestamp']) | tuple,
        )
        unit1.delete()
        unit2.delete()
