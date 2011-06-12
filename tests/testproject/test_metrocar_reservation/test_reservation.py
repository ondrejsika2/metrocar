'''
Created on 24.4.2010

@author: xaralis
'''
from nose.tools import raises

from datetime import datetime, timedelta

from metrocar.utils.models import SiteSettings
from metrocar.reservations.models import Reservation, ReservationError

from testproject.test_metrocar_reservation import ReservationEnabledTestCase
from testproject.helpers import CarEnabledWithoutReservationTestCase

from django.contrib.gis.geos import Point
from metrocar.tarification.models import Pricelist
from helpers import CarEnabledTestCase
from metrocar.cars.models import Journey

class TestReservation(ReservationEnabledTestCase):
    def test_0_validate_invalid_in_past(self):
        self.reservation.reserved_from = datetime.now() - timedelta(hours=1)
        val_res, val_errs = self.reservation.is_valid()
        self.assert_false(val_res)
        self.assert_true(len(val_errs) == 1)
        
    def test_1_validate_invalid_where_reserved_until_sooner(self):
        tmp = self.reservation.reserved_until
        self.reservation.reserved_until = self.reservation.reserved_from
        val_res, val_errs = self.reservation.is_valid()
        self.reservation.reserved_from = tmp
        self.assert_false(val_res)
        self.assert_true(len(val_errs) == 1)
        
    def test_2_validate_duration_limits(self):
        ss = SiteSettings.objects.get_current()
        self.reservation.reserved_until = self.reservation.reserved_from \
            + timedelta(seconds=(ss.reservation_min_duration - 1))
        val_res, val_errs = self.reservation.is_valid()
        self.assert_false(val_res)
        self.assert_true(len(val_errs) == 1)
        
        self.reservation.reserved_until = self.reservation.reserved_from \
            + timedelta(seconds=(ss.reservation_max_duration + 1))
        val_res, val_errs = self.reservation.is_valid()
        self.assert_false(val_res)
        self.assert_true(len(val_errs) == 1)
        
    def test_3_validate_account_limit(self):
        ss = SiteSettings.objects.get_current()
        pe = self.reservation.estimate_price()
        self.user.account.balance = ss.reservation_money_multiplier * pe - 100
        val_res, val_errs = self.reservation.is_valid()
        self.assert_false(val_res)
        print val_errs
        self.assert_true(len(val_errs) == 1)
        
    def test_4_conflicting_time(self):
        self.reservation.save()
        reservation = Reservation(
            reserved_from=(self.reservation.reserved_from + timedelta(seconds=1)),
            reserved_until=(self.reservation.reserved_until + timedelta(hours=1)),
            user=self.user,
            car=self.car
        )
        val_res, val_errs = reservation.is_valid()
        self.assert_false(val_res)
        self.assert_true(len(val_errs) == 1)
        
    def test_5_find_conflicts(self):
        self.reservation.save()
        reservation = Reservation(
            reserved_from=(self.reservation.reserved_from + timedelta(seconds=1)),
            reserved_until=(self.reservation.reserved_until + timedelta(hours=1)),
            user=self.user,
            car=self.car
        )
        conflicts = reservation.get_conflicts()
        self.assert_equals(len(conflicts), 1)
        self.assert_equals(conflicts[0].pk, self.reservation.pk)
        
    def test_6_is_running(self):
        self.reservation.reserved_from = (datetime.now() + timedelta(hours=1))
        self.assert_false(self.reservation.is_running())
        
        self.reservation.reserved_from = (datetime.now() - timedelta(hours=1))
        self.assert_true(self.reservation.is_running())
        
        self.reservation.finished = True
        self.assert_false(self.reservation.is_running())
        
    def test_7_ready_to_finish_no_dedicated_parking(self):
        # these are collected by reservation daemon and should not be able to 
        # finish
        self.car.dedicated_parking_only = False
        self.assert_false(self.reservation.ready_to_finish())
        
    def test_8_ready_to_finish_on_dedicated_parking(self):
        self.car.dedicated_parking_only = True
        self.car.last_position = Point(20.0, 20.0) # parking is 0.0 - 50.0 rect
        self.car.save()
        
        self.reservation.started = datetime.now() + timedelta(hours=1)
        self.reservation.save()
        self.assert_true(self.reservation.ready_to_finish())
        
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
        self.assert_true(self.reservation.get_pricelist())
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
        self.assert_equals(len(to_be_finished), 1)
        self.assert_equals(to_be_finished[0].pk, self.r4.pk)
    
    def test_1_running(self):
        running = Reservation.objects.running()
        self.assert_equals(len(running), len(Reservation.objects.all()) 
            - len(Reservation.objects.finished())
            - len(Reservation.objects.waiting_to_start()))
        
    def test_2_pending(self):
        pending = Reservation.objects.pending()
        self.assert_equals(len(pending), len(Reservation.objects.all()) 
            - len(Reservation.objects.finished()))
        self.assert_equals(pending[0].pk, self.r1.pk)
        
    def test_3_finished(self):
        finished = Reservation.objects.finished()
        self.assert_equals(len(finished), len(Reservation.objects.all()) 
            - len(Reservation.objects.pending()))
        self.assert_equals(finished[0].pk, self.r3.pk)
    
    
    
        