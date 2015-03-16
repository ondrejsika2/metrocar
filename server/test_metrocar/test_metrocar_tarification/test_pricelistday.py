'''
Created on 24.4.2010

@author: xaralis
'''
from datetime import date, time

from decimal import Decimal

from nose.tools import raises

from django.db.utils import IntegrityError

from metrocar.tarification.models import PricelistDay, PricelistDayTime

from helpers import CarEnabledTestCase

class TestPricelistDay(CarEnabledTestCase):
    
    @raises(IntegrityError)
    def test_0_clone_fails_for_same_day(self):
        try:
            pd = self.pricelist.pricelistday_set.all()[0]
            pd2 = pd.clone()
        except:
            raise IntegrityError
        
    def test_1_clone_succeeds_for_day_change(self):
        pd = self.pricelist.pricelistday_set.all()[0]
        pd2 = pd.clone(weekday_from=1)
        self.assertTrue(pd2)
        
        pd3 = pd2.clone(weekday_from=None, date=date(year=2010, month=1, day=1))
        self.assertTrue(pd3)
        
    def test_2_get_weekday_human(self):
        pd = self.pricelist.pricelistday_set.all()[0]
        self.assertTrue(isinstance(pd.get_weekday_human(1), unicode))
        
    def test_3_get_pricing_timeline_whole_day(self):
        pd, created = PricelistDay.objects.get_or_create(
            weekday_from=1,
            pricelist=self.pricelist
        )
        dt, created = PricelistDayTime.objects.get_or_create(
            car_unused_ratio=Decimal('1'), car_used_ratio=Decimal('2'), 
            late_return_ratio=Decimal('3'), time_from=time(hour=1),
            pricelist_day=pd                                                   
        )
        self.assertEquals(pd.get_pricing_timeline(), [{
            'from': time(hour=0),
            'till': time(hour=23, minute=59, second=59),
            'minutes': 24 * 60,
            'coefs': {
                'unused': Decimal('1') * self.pricelist.price_per_hour,
                'used': Decimal('2') * self.pricelist.price_per_hour,
                'late_return': Decimal('3') * self.pricelist.price_per_hour
            }
        }])
        pd.delete()
        dt.delete()
        
    def test_4_get_pricing_timeline_two_records(self):
        pd, created = PricelistDay.objects.get_or_create(
            weekday_from=1,
            pricelist=self.pricelist
        )
        dt, created = PricelistDayTime.objects.get_or_create(
            car_unused_ratio=Decimal('1'), car_used_ratio=Decimal('2'), 
            late_return_ratio=Decimal('3'), time_from=time(hour=1),
            pricelist_day=pd                                                   
        )
        dt2 = dt.clone(time_from=time(hour=11), car_unused_ratio=Decimal('10'))
        self.assertEquals(pd.get_pricing_timeline(), [
            {
                'from': time(hour=0),
                'till': time(hour=0, minute=59, second=59),
                'minutes': 59,
                'coefs': {
                    'unused': Decimal('10') * self.pricelist.price_per_hour,
                    'used': Decimal('2') * self.pricelist.price_per_hour,
                    'late_return': Decimal('3') * self.pricelist.price_per_hour
                }
            },
            {
                'from': time(hour=1),
                'till': time(hour=10, minute=59, second=59),
                'minutes': 599,
                'coefs': {
                    'unused': Decimal('1') * self.pricelist.price_per_hour,
                    'used': Decimal('2') * self.pricelist.price_per_hour,
                    'late_return': Decimal('3') * self.pricelist.price_per_hour
                }
            },
            {
                'from': time(hour=11),
                'till': time(hour=23, minute=59, second=59),
                'minutes': 779,
                'coefs': {
                    'unused': Decimal('10') * self.pricelist.price_per_hour,
                    'used': Decimal('2') * self.pricelist.price_per_hour,
                    'late_return': Decimal('3') * self.pricelist.price_per_hour
                }
            },
        ])
        
    