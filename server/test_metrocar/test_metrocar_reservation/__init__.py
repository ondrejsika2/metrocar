
from datetime import datetime, timedelta

from metrocar.reservations.models import Reservation

from test_metrocar.helpers import CarEnabledTestCase

class ReservationEnabledTestCase(CarEnabledTestCase):
    def setUp(self):
        super(ReservationEnabledTestCase, self).setUp()
        self.reservation = Reservation(
            reserved_from=(datetime.now() + timedelta(hours=1)),
            reserved_until=(datetime.now() + timedelta(hours=12)),
            user=self.user,
            car=self.car
        )