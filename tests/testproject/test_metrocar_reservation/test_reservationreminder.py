'''
Created on 24.4.2010

@author: xaralis
'''
from datetime import timedelta

from metrocar.reservations.models import ReservationReminder

from testproject.test_metrocar_reservation import ReservationEnabledTestCase

class TestReservationReminder(ReservationEnabledTestCase):
    def setUp(self):
        super(TestReservationReminder, self).setUp()
        self.reminder = ReservationReminder.objects.create_for_reservation(
            self.reservation, self.reservation.reserved_from - timedelta(minutes=20))
        