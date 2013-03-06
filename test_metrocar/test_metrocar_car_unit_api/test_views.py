import re
from datetime import datetime, timedelta
from decimal import Decimal

from djangosanetesting.cases import DatabaseTestCase, UnitTestCase

import geotrack.api

from metrocar.car_unit_api.testing_data import unit
from metrocar.car_unit_api.views import StoreLog, get_upcoming_reservations, reservation_user_data, reservation_data_for_car_unit, Reservations
from metrocar.reservations.models import Reservation
from metrocar.utils import Bunch
from metrocar.cars import testing_data as cars_testing_data
from metrocar.user_management.testing_data import create_user

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


class TestReservationData(UnitTestCase):

    def setUp(self):
        self.pw_hash = 'asdfadfa:sadfad:sdafafda'
        self.reservation = Bunch(
            user=Bunch(
                username='komarem',
                password=self.pw_hash,
            ),
            reserved_from=datetime(2012, 12, 12, 12, 12),
            reserved_until=datetime(2012, 12, 12, 12, 13),
            id = 11,
        )

    def test_user_data(self):
        self.assertEqual(reservation_user_data(self.reservation.user), {
            'username': 'komarem',
            'password': self.pw_hash,
        })

    def test_reservation_data(self):
        self.assertEqual(reservation_data_for_car_unit(self.reservation), {
            'user': reservation_user_data(self.reservation.user),
            'start': datetime(2012, 12, 12, 12, 12),
            'end': datetime(2012, 12, 12, 12, 13),
            'reservationId': 11,
        })


class TestReservationsView(DatabaseTestCase):

    @skipIfNotGeoEnabled
    def setUp(self):
        self.car = cars_testing_data.create()['cars'][0]
        self.unit = unit(123, car=self.car)
        self.user = create_user('asdf', 'asdf', 'First', 'Last')
        self.reservation = Reservation.objects.create(
            reserved_from=datetime.now() + timedelta(days=1),
            reserved_until=datetime.now() + timedelta(days=1, hours=4),
            user=self.user,
            car=self.car,
        )

    def tearDown(self):
        self.reservation.delete()
        self.user.delete()
        self.unit.delete()

    @property
    def view(self):
        return Reservations.as_view()

    def test_request(self):
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
            method='GET',
            body=data,
        )

        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"status": "ok"', response.content)
