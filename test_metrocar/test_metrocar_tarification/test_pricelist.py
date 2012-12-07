from datetime import time, date, datetime, timedelta
from decimal import Decimal

from metrocar.cars.models import Journey
from metrocar.tarification.models import PricelistDay, PricelistDayTime

from helpers import CarEnabledTestCase


class TestPricelist(CarEnabledTestCase):

    maxDiff = None

    def test_0_clone(self):
        pdays = self.pricelist.pricelistday_set.all()
        p2 = self.pricelist.clone()
        p2days = p2.pricelistday_set.all()
        self.assert_equals(len(pdays), len(p2days))

    def test_1_get_basic_price_dict(self):
        self.assert_equals(self.pricelist.get_basic_price_dict(), {
            'pickup_fee': 100,
            'price_per_km': 50,
            'price_per_hour_from': Decimal('1.6') * 10,
            'price_per_hour_till': Decimal('1.6') * 10
        })

        pdt = self.pricelist.pricelistday_set.all()[0].pricelistdaytime_set.all()[0]
        pdt.clone(time_from=time(hour=4), car_used_ratio=Decimal('5'))
        pdt.clone(time_from=time(hour=6), car_used_ratio=Decimal('0.1'))

        self.assert_equals(self.pricelist.get_basic_price_dict(), {
            'pickup_fee': 100,
            'price_per_km': 50,
            'price_per_hour_from': Decimal('0.1') * 10,
            'price_per_hour_till': Decimal('5') * 10
        })

    def test_2_get_pricelistday_for_date(self):
        pd1 = self.pricelist.pricelistday_set.all()[0]
        pd2 = pd1.clone(weekday_from=4)
        pd3 = pd1.clone(date=date(year=2010, month=1, day=1), weekday_from=None)

        #=======================================================================
        # We have records from monday (pd1), friday (pd2) and 01/01/2010 (pd3)
        #=======================================================================
        # test for date
        self.assert_equals(
            self.pricelist.get_pricelistday_for_date(date(year=2010, month=1, day=1)).pk,
            pd3.pk
        )
        # test for tuesday
        self.assert_equals(
            self.pricelist.get_pricelistday_for_date(date(year=2010, month=4, day=20)).pk,
            pd1.pk
        )
        # test for sunday
        self.assert_equals(
            self.pricelist.get_pricelistday_for_date(date(year=2010, month=4, day=25)).pk,
            pd2.pk
        )
        pd1.delete()
        pd3.delete()
        #=======================================================================
        # Now we only have record for friday
        #=======================================================================
        # test for monday
        self.assert_equals(
            self.pricelist.get_pricelistday_for_date(date(year=2010, month=4, day=19)).pk,
            pd2.pk
        )

    def test_3_get_pricing_summary(self):
        pd1 = self.pricelist.pricelistday_set.all()[0]
        pd2 = pd1.clone(weekday_from=4)
        pd3 = pd1.clone(date=date(year=2010, month=1, day=1), weekday_from=None)

        self.assert_equals(self.pricelist.get_pricing_summary(), {
            'rates': {
                'pickup_fee': self.pricelist.pickup_fee,
                'reservation_fee': self.pricelist.reservation_fee,
                'per_hour': self.pricelist.price_per_hour,
                'per_km': self.pricelist.price_per_km
            },
            'timeline': {
                'weekdays': [
                    ({'id': pd1.weekday_from, 'str': pd1.get_str_rep()}, pd1.get_pricing_timeline()),
                    ({'id': pd2.weekday_from, 'str': pd2.get_str_rep()}, pd2.get_pricing_timeline())
                ],
                'dates': [
                    ({'date': pd3.date}, pd3.get_pricing_timeline())
                ]
            }
        })

        #=======================================================================
        # Now only one weekday
        #=======================================================================
        pd1.delete()

        self.assert_equals(self.pricelist.get_pricing_summary(), {
            'rates': {
                'pickup_fee': self.pricelist.pickup_fee,
                'reservation_fee': self.pricelist.reservation_fee,
                'per_hour': self.pricelist.price_per_hour,
                'per_km': self.pricelist.price_per_km
            },
            'timeline': {
                'weekdays': [
                    ({'id': 0, 'str': PricelistDay.get_weekday_human(0)}, pd2.get_pricing_timeline())
                ],
                'dates': [
                    ({'date': pd3.date}, pd3.get_pricing_timeline())
                ]
            }
        })

    def test_4_count_journey_price_one_timeline_rec(self):
        #=======================================================================
        # First easy case, only one timeline rec and journey in one day
        #=======================================================================
        j = Journey(
            start_datetime=datetime(year=2010, month=4, day=25, hour=1, minute=0),
            end_datetime=datetime(year=2010, month=4, day=25, hour=2, minute=0),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            length = 100
        )
        pdt = self.pricelist.pricelistday_set.all()[0].pricelistdaytime_set.all()[0]
        self.assert_equals(self.pricelist.count_journey_price(j), {
            'total_price': pdt.car_used_ratio * self.pricelist.price_per_hour + 100 * self.pricelist.price_per_km,
            'km_price': 100 * self.pricelist.price_per_km,
            'time_price': pdt.car_used_ratio * self.pricelist.price_per_hour,
            'journey_parts': [{
                    'start': datetime(year=2010, month=4, day=25, hour=1, minute=0),
                    'end': datetime(year=2010, month=4, day=25, hour=2, minute=0),
                    'duration': timedelta(seconds=3600),
                    'price_per_hour': pdt.car_used_ratio * self.pricelist.price_per_hour,
                    'price': pdt.car_used_ratio * self.pricelist.price_per_hour
                }
            ]
        })

    def test_5_count_journey_price_multiple_timeline_rec(self):
        #=======================================================================
        # Multiple timeline records and journey in one day
        #=======================================================================
        j = Journey(
            start_datetime=datetime(year=2010, month=4, day=25, hour=1, minute=0),
            end_datetime=datetime(year=2010, month=4, day=25, hour=10, minute=0),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            length = 100
        )
        pdt = self.pricelist.pricelistday_set.all()[0].pricelistdaytime_set.all()[0]
        pdt2 = pdt.clone(time_from=time(hour=6), car_used_ratio=Decimal('4.0'))
        self.assert_equals(self.pricelist.count_journey_price(j), {
            'total_price': (5 * pdt.car_used_ratio + 4 * pdt2.car_used_ratio) * self.pricelist.price_per_hour + 100 * self.pricelist.price_per_km,
            'km_price': 100 * self.pricelist.price_per_km,
            'time_price': (5 * pdt.car_used_ratio + 4 * pdt2.car_used_ratio) * self.pricelist.price_per_hour,
            'journey_parts': [{
                    'start': datetime(year=2010, month=4, day=25, hour=1, minute=0),
                    'end': datetime(year=2010, month=4, day=25, hour=6, minute=0),
                    'duration': timedelta(seconds=5 * 3600),
                    'price_per_hour': pdt.car_used_ratio * self.pricelist.price_per_hour,
                    'price': pdt.car_used_ratio * self.pricelist.price_per_hour * 5
                },
                {
                    'start': datetime(year=2010, month=4, day=25, hour=6, minute=0),
                    'end': datetime(year=2010, month=4, day=25, hour=10, minute=0),
                    'duration': timedelta(seconds=4 * 3600),
                    'price_per_hour': pdt2.car_used_ratio * self.pricelist.price_per_hour,
                    'price': pdt2.car_used_ratio * self.pricelist.price_per_hour * 4
                }
            ]
        })

    def test_6_count_journey_price_multiple_timeline_rec_multiple_days(self):
        #=======================================================================
        # Journey will be split in two days
        #=======================================================================
        j = Journey(
            start_datetime=datetime(year=2010, month=4, day=25, hour=1, minute=0),
            end_datetime=datetime(year=2010, month=4, day=26, hour=10, minute=0),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            length = 100
        )
        pd1 = self.pricelist.pricelistday_set.all()[0]
        pd1t1 = self.pricelist.pricelistday_set.all()[0].pricelistdaytime_set.all()[0]

        pd2 = pd1.clone(date=date(year=2010, month=4, day=26), weekday_from=None)

        pd2t1 = PricelistDayTime.objects.get(pricelist_day=pd2)
        pd2t1.car_used_ratio = Decimal('4.0')
        pd2t1.save()

        result = self.pricelist.count_journey_price(j)
        expected = {
            'total_price': (23 * pd1t1.car_used_ratio + 10 * pd2t1.car_used_ratio) * self.pricelist.price_per_hour + 100 * self.pricelist.price_per_km,
            'km_price': 100 * self.pricelist.price_per_km,
            'time_price': (23 * pd1t1.car_used_ratio + 10 * pd2t1.car_used_ratio) * self.pricelist.price_per_hour,
            'journey_parts': [{
                    'start': datetime(year=2010, month=4, day=25, hour=1, minute=0),
                    'end': datetime(year=2010, month=4, day=26, hour=0),
                    'duration': timedelta(seconds=23 * 3600),
                    'price_per_hour': pd1t1.car_used_ratio * self.pricelist.price_per_hour,
                    'price': pd1t1.car_used_ratio * self.pricelist.price_per_hour * 23
                },
                {
                    'start': datetime(year=2010, month=4, day=26, hour=0, minute=0),
                    'end': datetime(year=2010, month=4, day=26, hour=10, minute=0),
                    'duration': timedelta(seconds=10 * 3600),
                    'price_per_hour': pd2t1.car_used_ratio * self.pricelist.price_per_hour,
                    'price': pd2t1.car_used_ratio * self.pricelist.price_per_hour * 10
                }
            ]
        }
        self.assert_equals(result, expected)

