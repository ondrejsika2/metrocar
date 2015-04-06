'''
Created on 21.4.2010

@author: xaralis
'''
from datetime import datetime, timedelta

from test_metrocar.helpers import CarEnabledTestCase
from metrocar.reservations.models import Reservation
from metrocar.cars.models import Journey, Car

class TestCar(CarEnabledTestCase):

    def test_is_user_allowed(self):
        self.assertTrue(self.car.is_user_allowed(self.user, datetime(year=2010, month=1, day=1, hour=10, minute=30)))
        self.assertFalse(self.car.is_user_allowed(self.user, datetime(year=2010, month=1, day=1, hour=9, minute=30)))
        self.assertFalse(self.car.is_user_allowed(self.user, datetime(year=2010, month=1, day=1, hour=11, minute=30)))

        self.user.user_card.is_service_card = True
        self.user.user_card.save()
        self.assertTrue(self.car.is_user_allowed(self.user, datetime(year=2010, month=1, day=1, hour=11, minute=30)))

    def test_get_allowed_users(self):
        self.user.user_card.is_service_card = True
        self.user.user_card.save()
        self.assertTrue(len(self.car.get_allowed_users()) > 0)

    def test_get_upcoming_reservations(self):
        r = Reservation.objects.create(
            reserved_from=(datetime.now() + timedelta(minutes=1)),
            reserved_until=(datetime.now() + timedelta(hours=1)),
            car=self.car,
            user=self.user
        )
        self.assertEquals(
            len(self.car.get_upcoming_reservations(format='qset')), 1)

    def test_get_current_journey(self):
        j = Journey.objects.create(
            start_datetime=(datetime.now() - timedelta(minutes=1)),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP
        )
        self.assertNotEquals(self.car.get_current_journey(), None)
        j.end_datetime = datetime.now() - timedelta(seconds=1)
        j.save()
        self.assertEquals(self.car.get_current_journey(), None)

