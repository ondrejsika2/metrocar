import re
from datetime import datetime
from decimal import Decimal

from djangosanetesting.cases import DatabaseTestCase

import geotrack.api

from metrocar.car_unit_api.testing_data import unit
from metrocar.car_unit_api.views import StoreLog
from metrocar.utils import Bunch

from test_metrocar.helpers import skipIfNotGeoEnabled


class TestStoreLogDataValidation(DatabaseTestCase):

    @skipIfNotGeoEnabled
    def setUp(self):
        self.unit = unit(123)

    @property
    def view(self):
        return StoreLog.as_view()

    def test_valid_request(self):

        data = """{
            "unit_id": %(unit_id)s,
            "secret_key": "%(secret_key)s",
            "entries": [
                {
                    "timestamp": "2012-10-27T17:18:38.638Z",
                    "location": [50.05323, 14.45277],
                    "event": "UNLOCKED",
                    "odometer": 98746.12
                },
                {
                    "timestamp": "2012-10-27T17:18:39",
                    "location": [50.05323, 14.45276]
                }
            ]
        }""" % dict(unit_id=self.unit.unit_id, secret_key=self.unit.secret_key)

        request = Bunch(
            method='POST',
            body=data,
        )

        response = self.view(request)

        print response.content

        self.assertEqual(response.status_code, 200)
        self.assertEqual(re.sub('\s+', '', response.content), '{"status":"ok"}')

        stored = geotrack.api.query('all')

        self.assertEqual(len(stored), 2)

        self.assertEqual(stored[0]['unit_id'], self.unit.unit_id)
        self.assertEqual(stored[0]['timestamp'],
            datetime(2012, 10, 27, 17, 18, 38, 638000))
        self.assertEqual(stored[0]['location'], (50.05323, 14.45277))
        self.assertEqual(stored[0]['event'], 'UNLOCKED')
        self.assertEqual(stored[0]['odometer'], Decimal('98746.12'))

        self.assertEqual(stored[1]['unit_id'], self.unit.unit_id)
        self.assertEqual(stored[1]['timestamp'],
            datetime(2012, 10, 27, 17, 18, 39))
        self.assertEqual(stored[1]['location'], (50.05323, 14.45276))

        geotrack.backends.get_backend().flush()

    def test_invalid_request(self):

        data = """{
            "unit_id": %(unit_id)s,
            "secret_key": "%(secret_key)s",
            "entries": [
                {
                    "timestamp": "2012-10-27T17:18:38.638Z",
                    "location": [50.05323, 14.45277],
                    "event": "UNLOCKED"
                },
                {
                    "location": [50.05323, 14.45276]
                }
            ]
        }""" % dict(unit_id=self.unit.unit_id, secret_key=self.unit.secret_key)

        request = Bunch(
            method='POST',
            body=data,
        )

        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn('"status": "error"', response.content)

        stored = geotrack.api.query('all')

        self.assertEqual(len(stored), 0)
