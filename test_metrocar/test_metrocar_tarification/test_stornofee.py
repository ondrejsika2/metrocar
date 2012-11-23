'''
Created on 24.4.2010

@author: xaralis
'''
from datetime import datetime, timedelta

from nose.tools import raises

from django.core.exceptions import ImproperlyConfigured

from metrocar.tarification.models import StornoFeeTimeline, StornoFee
from metrocar.reservations.models import Reservation

from helpers import CarEnabledTestCase

class TestStornoFee(CarEnabledTestCase):
    def setUp(self):
        super(TestStornoFee, self).setUp()
        self.sft1, created = StornoFeeTimeline.objects.get_or_create(
            preceeding_time_from=600,
            price=20
        )
        self.sft2, created = StornoFeeTimeline.objects.get_or_create(
            preceeding_time_from=2400,
            price=50
        )
        self.sft3, created = StornoFeeTimeline.objects.get_or_create(
            preceeding_time_from=7200,
            price=100
        )
        self.reservation, created = Reservation.objects.get_or_create(
            reserved_from=datetime(year=2010, month=1, day=1, hour=1),
            reserved_until=datetime(year=2010, month=1, day=1, hour=5),
            user=self.user,
            car=self.car
        )
        
    @raises(AssertionError)
    def test_0_get_record_for_reservation_too_late_to_cancel(self):
        StornoFee.objects.get_record_for_reservation(self.reservation,
            datetime(year=2010, month=1, day=1, hour=0, minute=55))
        
        self.assert_true(False)
        
        raise ValueError()
        
    @raises(ImproperlyConfigured)
    def test_1_get_record_for_reservation_improperly_configured(self):
        self.sft1.delete()
        self.sft2.delete()
        self.sft3.delete()
        StornoFee.objects.get_record_for_reservation(self.reservation,
            datetime(year=2010, month=1, day=1, hour=0))
        
    def test_2_get_record_for_reservation(self):
        r = StornoFee.objects.get_record_for_reservation(self.reservation,
            datetime(year=2010, month=1, day=1, hour=0, minute=35))
        self.assert_equals(r.pk, self.sft1.pk)
        
        r = StornoFee.objects.get_record_for_reservation(self.reservation,
            datetime(year=2009, month=12, day=31, hour=20, minute=30))
        self.assert_equals(r.pk, self.sft3.pk)
        
    @raises(AssertionError)
    def test_3_create_for_reservation(self):
        self.reservation.finished = True
        r = StornoFee.objects.create_for_reservation(self.reservation)
        