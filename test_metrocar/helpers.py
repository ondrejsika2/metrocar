from decimal import Decimal
from datetime import datetime, date, time

from django.conf import settings
from django.contrib.gis.geos.polygon import Polygon
from django.contrib.sites.models import Site
from django.utils.unittest import TestCase

from djangosanetesting.cases import DatabaseTestCase

from metrocar.cars.models import CarModelManufacturer, CarType, Fuel, \
    CarModel, Car, CarColor, Parking
from metrocar.subsidiaries.models import Subsidiary
from metrocar.user_management.models import MetrocarUser
from metrocar.reservations.models import Reservation
from metrocar.tarification.models import Pricelist, PricelistDay,\
    PricelistDayTime


def get_subsidiary():
    return Subsidiary.objects.get_current()

class SubsidiaryEnabledTestCase(DatabaseTestCase):
    def setUp(self):
        super(SubsidiaryEnabledTestCase, self).setUp()
        self.subsidiary = get_subsidiary()

class UserEnabledTestCase(DatabaseTestCase):
    def setUp(self):
        super(UserEnabledTestCase, self).setUp()
        try:
            self.user = MetrocarUser.objects.with_inactive().get(username='some_username')
            self.user.is_active = True
            self.user.account.balance = Decimal('100000.0')
            self.user.save()
        except MetrocarUser.DoesNotExist:
            self.user = MetrocarUser.objects.create_user('some_username', 'test@test.cz',
                'testpass', is_active=True)
            self.user.account.balance = Decimal('100000.0')

def get_cars(**kwargs):
    manufacturer, created = CarModelManufacturer.objects.get_or_create(slug='slug', name='title')
    type, created = CarType.objects.get_or_create(type='type')
    fuel, created = Fuel.objects.get_or_create(title='title')
    color, created = CarColor.objects.get_or_create(color='blue')
    car_model, created = CarModel.objects.get_or_create(
        engine='engine', seats_count=1, storage_capacity=1, name='title',
        type=type, main_fuel=fuel, manufacturer=manufacturer
    )

    defaults = {
        'active': True,
        'manufacture_date': datetime.now(),
        'model': car_model,
        'color': color,
        'home_subsidiary': get_subsidiary(),
    }
    defaults.update(**kwargs)

    try:
        car = Car.objects.get(registration_number='123123')
    except Car.DoesNotExist:
        car = Car.objects.create(registration_number='123123', **defaults)

    parking = Parking.objects.get_or_create(name='Test', places_count=200,
        land_registry_number='100', street='Test', city='Praha',
        polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))
        )
    )

    return car_model, car, parking


class CarEnabledWithoutReservationTestCase(UserEnabledTestCase):
    def setUp(self):
        super(CarEnabledWithoutReservationTestCase, self).setUp()
        self.car_model, self.car, self.parking = get_cars()

        self.pricelist, created = Pricelist.objects.get_or_create(
            available=True,
            name='Test pricelist',
            pickup_fee=100,
            price_per_hour=10,
            price_per_km=50,
            reservation_fee=200,
            valid_from=date(day=1, month=1, year=2000),
            model=self.car_model
        )
        pd, created = PricelistDay.objects.get_or_create(
            weekday_from=0,
            pricelist=self.pricelist
        )
        PricelistDayTime.objects.get_or_create(
            car_unused_ratio=Decimal('0.5'), car_used_ratio=Decimal('1.6'),
            late_return_ratio=Decimal('5'), time_from=time(hour=0),
            pricelist_day=pd
        )

class CarEnabledTestCase(CarEnabledWithoutReservationTestCase):
    def setUp(self):
        super(CarEnabledTestCase, self).setUp()
        self.reservation, created = Reservation.objects.get_or_create(
            reserved_from=datetime(year=2010, month=1, day=1, hour=10),
            reserved_until=datetime(year=2010, month=1, day=1, hour=11),
            car=self.car,
            user=self.user
        )


# This is pretty retarded, but needed for test-skipping compatible with nose
# in python < 2.7 -- we need to raise nose's SkipTest exception instead of
# the one from Django

from nose.plugins.skip import SkipTest
from functools import wraps


def _id(obj):
    return obj


def skip(reason):
    """
    Unconditionally skip a test.
    """
    def decorator(test_item):
        if not (isinstance(test_item, type) and issubclass(test_item, TestCase)):
            @wraps(test_item)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)
            test_item = skip_wrapper

        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item
    return decorator


def skipIf(condition, reason):
    """
    Skip a test if the condition is true.
    """
    if condition:
        return skip(reason)
    return _id


skipIfNotGeoEnabled = skipIf(not settings.GEO_ENABLED, 'not geo-enabled')
