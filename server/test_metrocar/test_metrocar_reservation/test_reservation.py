from datetime import datetime, timedelta

import django.test

from metrocar.cars.models import Car
from metrocar.reservations.models import Reservation
from metrocar.user_management.models import MetrocarUser
from test_metrocar.test_metrocar_cars.fixtures import create_car_1
from test_metrocar.test_metrocar_reservation.fixtures import create_reservation_1
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1
from metrocar.utils.models import SiteSettings

#
class TestReservation(django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        Reservation.objects.all().delete()
        MetrocarUser.objects.all().delete()
        Car.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Reservation.objects.all().delete()
        MetrocarUser.objects.all().delete()
        Car.objects.all().delete()

    def setUp(self):
        self.reservation_1 = create_reservation_1()
        self.user_1 = create_user_1()
        self.car_1 = create_car_1()

    def test_0_validate_invalid_in_past(self):
        self.reservation_1.reserved_from = datetime.utcnow() - timedelta(hours=1)
        val_res, val_errs = self.reservation_1.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_1_validate_invalid_where_reserved_until_sooner(self):
        tmp = self.reservation_1.reserved_until
        self.reservation_1.reserved_until = self.reservation_1.reserved_from
        val_res, val_errs = self.reservation_1.is_valid()
        self.reservation_1.reserved_from = tmp
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)
#
    def test_2_validate_duration_limits(self):
        ss = SiteSettings.objects.get_current()
        self.reservation_1.reserved_until = self.reservation_1.reserved_from \
            + timedelta(seconds=(ss.reservation_min_duration - 1))
        val_res, val_errs = self.reservation_1.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

        self.reservation_1.reserved_until = self.reservation_1.reserved_from \
            + timedelta(seconds=(ss.reservation_max_duration + 1))
        val_res, val_errs = self.reservation_1.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_3_conflicting_time(self):
        self.reservation_1.save()
        reservation = Reservation(
            reserved_from=(self.reservation_1.reserved_from + timedelta(seconds=1)),
            reserved_until=(self.reservation_1.reserved_until + timedelta(hours=1)),
            user=self.user_1,
            car=self.car_1
        )
        val_res, val_errs = reservation.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_4_is_running(self):
        self.reservation_1.reserved_from = (datetime.now() + timedelta(hours=1))
        self.assertFalse(self.reservation_1.is_running())

        self.reservation_1.reserved_from = (datetime.now() - timedelta(hours=1))
        self.assertTrue(self.reservation_1.is_running())

        self.reservation_1.finished = True
        self.assertFalse(self.reservation_1.is_running())

    def test_5_ready_to_finish_no_dedicated_parking(self):
        # these are collected by reservation daemon and should not be able to
        # finish
        self.car_1.dedicated_parking_only = False
        self.assertFalse(self.reservation_1.ready_to_finish())

