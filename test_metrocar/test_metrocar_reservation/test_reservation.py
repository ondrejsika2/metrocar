from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.gis.geos import Point
import django.test

from nose.tools import raises

from metrocar.car_unit_api.testing_data import unit
from metrocar.car_unit_api.views import store as api_store
from metrocar.cars import testing_data as cars_testing_data
from metrocar.cars.models import Journey
from metrocar.reservations.models import Reservation, ReservationError
from metrocar.tarification.models import Pricelist
from metrocar.tarification.testing_data import create_pricelist
from metrocar.user_management.models import Account
from metrocar.user_management.testing_data import create_user
from metrocar.utils import Bunch
from metrocar.utils.models import SiteSettings

import geotrack

from test_metrocar.test_metrocar_reservation import ReservationEnabledTestCase
from test_metrocar.helpers import CarEnabledWithoutReservationTestCase, skipIfNotGeoEnabled, CarEnabledTestCase


class TestReservation(ReservationEnabledTestCase):
    def test_0_validate_invalid_in_past(self):
        self.reservation.reserved_from = datetime.now() - timedelta(hours=1)
        val_res, val_errs = self.reservation.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_1_validate_invalid_where_reserved_until_sooner(self):
        tmp = self.reservation.reserved_until
        self.reservation.reserved_until = self.reservation.reserved_from
        val_res, val_errs = self.reservation.is_valid()
        self.reservation.reserved_from = tmp
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_2_validate_duration_limits(self):
        ss = SiteSettings.objects.get_current()
        self.reservation.reserved_until = self.reservation.reserved_from \
            + timedelta(seconds=(ss.reservation_min_duration - 1))
        val_res, val_errs = self.reservation.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

        self.reservation.reserved_until = self.reservation.reserved_from \
            + timedelta(seconds=(ss.reservation_max_duration + 1))
        val_res, val_errs = self.reservation.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_3_validate_account_limit(self):
        ss = SiteSettings.objects.get_current()
        pe = self.reservation.estimate_price()
        self.user.account.balance = ss.reservation_money_multiplier * pe - 100
        val_res, val_errs = self.reservation.is_valid()
        self.assertFalse(val_res)
        print val_errs
        self.assertTrue(len(val_errs) == 2)

    def test_4_conflicting_time(self):
        self.reservation.save()
        reservation = Reservation(
            reserved_from=(self.reservation.reserved_from + timedelta(seconds=1)),
            reserved_until=(self.reservation.reserved_until + timedelta(hours=1)),
            user=self.user,
            car=self.car
        )
        val_res, val_errs = reservation.is_valid()
        self.assertFalse(val_res)
        self.assertTrue(len(val_errs) == 1)

    def test_5_find_conflicts(self):
        self.reservation.save()
        reservation = Reservation(
            reserved_from=(self.reservation.reserved_from + timedelta(seconds=1)),
            reserved_until=(self.reservation.reserved_until + timedelta(hours=1)),
            user=self.user,
            car=self.car
        )
        conflicts = reservation.get_conflicts()
        self.assertEquals(len(conflicts), 1)
        self.assertEquals(conflicts[0].pk, self.reservation.pk)

    def test_6_is_running(self):
        self.reservation.reserved_from = (datetime.now() + timedelta(hours=1))
        self.assertFalse(self.reservation.is_running())

        self.reservation.reserved_from = (datetime.now() - timedelta(hours=1))
        self.assertTrue(self.reservation.is_running())

        self.reservation.finished = True
        self.assertFalse(self.reservation.is_running())

    def test_7_ready_to_finish_no_dedicated_parking(self):
        # these are collected by reservation daemon and should not be able to
        # finish
        self.car.dedicated_parking_only = False
        self.assertFalse(self.reservation.ready_to_finish())

    @skipIfNotGeoEnabled
    def test_8_ready_to_finish_on_dedicated_parking(self):
        self.car.dedicated_parking_only = True
        self.car.save()

        unit_id = 681639879
        unit(unit_id, car=self.car)

        geotrack.api.store(unit_id,
            timestamp=datetime.now(),
            # parking is 0.0 - 50.0 rect
            location=(20.0, 20.0))

        self.reservation.started = datetime.now() + timedelta(hours=1)
        self.reservation.save()
        self.assertTrue(self.reservation.ready_to_finish())

    @raises(ReservationError)
    def test_9_get_pricelist_fails_for_nonexistent(self):
        self.pricelist.delete()
        self.reservation.save()
        self.reservation.get_pricelist()
        self.reservation.delete()

    @raises(ReservationError)
    def test_a0_get_pricelist_fails_for_invalid(self):
        self.pricelist.available = False
        self.pricelist.save()
        self.reservation.save()
        self.reservation.get_pricelist()
        self.reservation.delete()

    def test_a1_pricelist_succeeds_for_invalid_when_finished(self):
        # we can use invalid pricelist when referring to past reservations
        self.pricelist.available = False
        self.pricelist.save()
        self.reservation.finished = True
        self.reservation.save()
        self.assertTrue(self.reservation.get_pricelist())
        self.pricelist.delete()
        self.reservation.delete()


class TestReservationManager(CarEnabledWithoutReservationTestCase):
    def setUp(self):
        super(TestReservationManager, self).setUp()

        for r in Reservation.objects.all():
            r.delete()

        # pending
        self.r1 = Reservation(
            reserved_from=(datetime.now() + timedelta(hours=1)),
            reserved_until=(datetime.now() + timedelta(hours=12)),
            user=self.user,
            car=self.car
        )
        self.r1.save()
        # running
        self.r2 = Reservation(
            reserved_from=(datetime.now() - timedelta(hours=1)),
            reserved_until=(datetime.now() + timedelta(hours=12)),
            started=datetime.now(),
            user=self.user,
            car=self.car
        )
        self.r2.save()
        self.r2j = Journey(
            start_datetime=(datetime.now() - timedelta(minutes=5)),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            reservation=self.r2
        )
        # finished
        self.r3 = Reservation(
            reserved_from=(datetime.now() + timedelta(hours=1)),
            reserved_until=(datetime.now() + timedelta(hours=2)),
            started=datetime.now(),
            ended=(datetime.now() + timedelta(hours=2)),
            finished=True,
            user=self.user,
            car=self.car
        )
        self.r3.save()
        # to be finished
        self.r4 = Reservation(
            reserved_from=(datetime.now() - timedelta(hours=2)),
            reserved_until=(datetime.now()),
            started=(datetime.now() - timedelta(hours=1)),
            user=self.user,
            car=self.car
        )
        self.r4.save()

    def tearDown(self):
        super(TestReservationManager, self).tearDown()
        self.r1.delete()
        self.r2.delete()
        self.r3.delete()
        self.r4.delete()

    def test_0_to_be_finished(self):
        to_be_finished = Reservation.objects.to_be_finished()
        self.assertEquals(len(to_be_finished), 1)
        self.assertEquals(to_be_finished[0].pk, self.r4.pk)

    def test_1_running(self):
        running = Reservation.objects.running()
        self.assertEquals(len(running), len(Reservation.objects.all())
            - len(Reservation.objects.finished())
            - len(Reservation.objects.waiting_to_start()))

    def test_2_pending(self):
        pending = Reservation.objects.pending()
        self.assertEquals(len(pending), len(Reservation.objects.all())
            - len(Reservation.objects.finished()))
        self.assertEquals(pending[0].pk, self.r1.pk)

    def test_3_finished(self):
        finished = Reservation.objects.finished()
        self.assertEquals(len(finished), len(Reservation.objects.all())
            - len(Reservation.objects.pending()))
        self.assertEquals(finished[0].pk, self.r3.pk)


class TestGeoEnabledReservationIntegration(DatabaseTestCase):

    def test_complete_process(self):

        # there is a user
        user = create_user('some_user', 'some_password', 'Some', 'Name')

        # there is a car with a car unit
        car = cars_testing_data.create()['cars'][0]
        unit_id = 456789
        car_unit = unit(unit_id, car)

        # a price list definition for the car
        prices = dict(
            pickup_fee=11,
            price_per_hour=11,
            price_per_km=15,
            reservation_fee=17,
        )
        price_list = create_pricelist(car.model, **prices)

        # user has a reservation
        r_from = datetime(2012, 12, 12, 10)
        r_until = datetime(2012, 12, 12, 12)
        reservation = Reservation.objects.create(
            user=user,
            car=car,
            reserved_from=r_from,
            reserved_until=r_until,
        )

        # data arrive from car unit
        api_store(unit_id, [
            dict(
                timestamp=datetime(2012, 12, 12, 11, 1),
                location=(14, 50),
                odometer=10000,
            ),
            dict(
                timestamp=datetime(2012, 12, 12, 11, 5),
                location=(14, 51),
                odometer=10010,
            ),
            dict(
                timestamp=datetime(2012, 12, 12, 11, 9),
                location=(14, 52),
                odometer=10030,
            ),
        ])

        # reservation is finished (by a daemon)
        reservation.finish(
            finish_datetime=datetime(2012, 12, 12, 12),
            by_daemon=True)

        # appropriate amount of money is deducted from user's account
        account = Account.objects.get(user=user)
        self.assertEquals(account.balance, -Decimal(str(sum((
            prices['pickup_fee'],
            prices['reservation_fee'],
            30 * prices['price_per_km'],
            2 * prices['price_per_hour'],
        )))))

        reservation.delete()
        user.delete()
        car_unit.delete()
        price_list.delete()
