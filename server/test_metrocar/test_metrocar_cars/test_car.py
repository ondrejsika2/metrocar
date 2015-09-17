from datetime import datetime, timedelta
from metrocar.user_management.models import MetrocarUser
from metrocar.reservations.models import Reservation
from metrocar.cars.models import Journey, Car
import django.test
from test_metrocar.test_metrocar_cars.fixtures import create_car_1, create_pricelist_1
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1


class TestCar(django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        Car.objects.all().delete()
        MetrocarUser.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Car.objects.all().delete()
        MetrocarUser.objects.all().delete()

    def setUp(self):
        self.car_1 = create_car_1()
        create_pricelist_1(car_model=self.car_1.model)
        self.user_1 = create_user_1()

    def test_is_user_allowed(self):
        self.assertFalse(self.car_1.is_user_allowed(self.user_1, datetime(year=2010, month=1, day=1, hour=9, minute=30)))
        self.assertFalse(self.car_1.is_user_allowed(self.user_1, datetime(year=2010, month=1, day=1, hour=11, minute=30)))

        self.user_1.user_card.is_service_card = True
        self.user_1.user_card.save()
        self.assertTrue(self.car_1.is_user_allowed(self.user_1, datetime(year=2010, month=1, day=1, hour=11, minute=30)))

    def test_get_allowed_users(self):
        self.user_1.user_card.is_service_card = True
        self.user_1.user_card.save()
        self.assertTrue(len(self.car_1.get_allowed_users()) > 0)

    def test_get_upcoming_reservations(self):
        r = Reservation.objects.create(
            reserved_from=(datetime.now() + timedelta(minutes=1)),
            reserved_until=(datetime.now() + timedelta(hours=1)),
            car=self.car_1,
            user=self.user_1
        )
        self.assertEquals(
            len(self.car_1.get_upcoming_reservations(format='qset')), 1)

    def test_get_current_journey(self):
        j = Journey.objects.create(
            start_datetime=(datetime.now() - timedelta(minutes=1)),
            car=self.car_1,
            user=self.user_1,
            type=Journey.TYPE_TRIP
        )
        self.assertNotEquals(self.car_1.get_current_journey(), None)
        j.end_datetime = datetime.now() - timedelta(seconds=1)
        j.save()
        self.assertEquals(self.car_1.get_current_journey(), None)


