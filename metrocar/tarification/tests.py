"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import datetime, date, time
from decimal import Decimal

from django.test import TestCase

from metrocar.tarification.models import *
from metrocar.cars.tests import create_cars_dummy_models

class PricelistTest(TestCase):
    def setUp(self):
        self.manufacturer, self.type, self.fuel, self.model = create_cars_dummy_models()
        
        self.pricelist = Pricelist.objects.create(
            name='Test pricelist',
            pickup_fee=100,
            price_per_hour=10,
            price_per_km=50,
            reservation_fee=200,
            valid_from=date(day=1, month=1, year=2000),
            model=self.model
        )
        
        self.pricelist2 = Pricelist.objects.create(
            name='Test pricelist',
            pickup_fee=100,
            price_per_hour=10,
            price_per_km=50,
            reservation_fee=200,
            valid_from=date(day=1, month=1, year=2000),
            model=self.model
        )
        
        self.pd_date1 = PricelistDay.objects.create(
            date=date(day=2, month=1, year=2000),
            pricelist=self.pricelist
        )
        self.pd_date1_time1 = PricelistDayTime.objects.create(
            car_unused_ratio=Decimal('0.8'), car_used_ratio=Decimal('1.2'), late_return_ratio=Decimal('3'),
            time_from=time(hour=10), pricelist_day=self.pd_date1                                                   
        )
        
        self.pd_weekday1 = PricelistDay.objects.create(
            weekday_from=3,
            pricelist=self.pricelist
        )
        self.pd_weekday1_time1 = PricelistDayTime.objects.create(
            car_unused_ratio=Decimal('0.5'), car_used_ratio=Decimal('1.6'), late_return_ratio=Decimal('5'),
            time_from=time(hour=0), pricelist_day=self.pd_weekday1                                                   
        )
        self.pd_weekday2 = PricelistDay.objects.create(
            weekday_from=5,
            pricelist=self.pricelist
        )
        self.pd_weekday2_time1 = PricelistDayTime.objects.create(
            car_unused_ratio=Decimal('0.8'), car_used_ratio=Decimal('1.2'), late_return_ratio=Decimal('3'),
            time_from=time(hour=23), pricelist_day=self.pd_weekday2                                                   
        )
        self.pd_weekday2_time2 = PricelistDayTime.objects.create(
            car_unused_ratio=Decimal('0.8'), car_used_ratio=Decimal('1.2'), late_return_ratio=Decimal('3'),
            time_from=time(hour=6), pricelist_day=self.pd_weekday2                                                   
        )
        
    def test_pricelistday_timeline(self):
        self.assertEquals(self.pd_weekday2.get_pricing_timeline(), [
            ( time(hour=0), { 'unused': 8, 'used': 12, 'late_return': 30 } ),
            ( self.pd_weekday2_time2.time_from, { 'unused': 8, 'used': 12, 'late_return': 30 } ),
            ( self.pd_weekday2_time1.time_from, { 'unused': 8, 'used': 12, 'late_return': 30 } ),
        ])
        
    def test_pricelist(self):
        self.assertEquals(
            self.pricelist.get_pricing_for_date(date(day=2, month=1, year=2000)),
            self.pd_date1.get_pricing_timeline()
        )
        
        self.assertEquals(
            self.pricelist.get_pricing_for_date(date(day=1, month=1, year=2000)),
            self.pd_weekday2.get_pricing_timeline()
        )
        
        self.assertRaises(
            PricelistAssertionError,
            self.pricelist2.get_pricing_for_date,
            date_to_find=date(day=1, month=1, year=2000)
        )
        
        summary = self.pricelist.get_pricing_summary()
        self.assertEquals(len(summary), 2)
        self.assertEquals(len(summary['rates']), 4)
        self.assertEquals(len(summary['timeline']['dates']), 1)
        self.assertEquals(len(summary['timeline']['weekdays']), 3) # filled up with monday
        
    def test_clone(self):
        self.assertEquals(self.pricelist2.name, self.pricelist2.clone().name)
        self.assertEquals(self.pricelist.get_pricing_summary(), self.pricelist.clone().get_pricing_summary())
        
        pricelist3 = Pricelist.objects.create(
            name='Test pricelist',
            pickup_fee=200,
            price_per_hour=10,
            price_per_km=50,
            reservation_fee=200,
            valid_from=date(day=1, month=1, year=2000),
            model=self.model
        )
        
        self.assertEquals(pricelist3.pickup_fee, self.pricelist2.clone(pickup_fee=200).pickup_fee)
        