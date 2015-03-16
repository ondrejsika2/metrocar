from nose.tools import raises

from datetime import datetime, timedelta

from test_metrocar.helpers import CarEnabledTestCase
from metrocar.reservations.models import Reservation
from metrocar.cars.models import Journey


class TestJourney(CarEnabledTestCase):
    def setUp(self):
        super(TestJourney, self).setUp()
        self.journey, created = Journey.objects.get_or_create(
            start_datetime=(datetime.now() - timedelta(minutes=1)),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP
        )

    @raises(AssertionError)
    def test_is_valid_active_conflict(self):
        j = Journey(
            start_datetime=(datetime.now() - timedelta(minutes=1)),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP
        )
        j.is_valid()

    @raises(AssertionError)
    def test_is_valid_wrong_times(self):
        j = Journey(
            start_datetime=(datetime.now() - timedelta(minutes=50)),
            end_datetime=(datetime.now() - timedelta(minutes=100)),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP
        )
        j.is_valid()

    def test_get_pricing_info_no_reservation(self):
        self.assertEquals(self.journey.get_pricing_info(), None)

    def test_is_finished(self):
        self.assertEquals(self.journey.is_finished(), False)
        self.journey.end_datetime = datetime.now()
        self.journey.save()
        self.assertEquals(self.journey.is_finished(), True)

    def test_get_current_for_car_user_card(self):
        self.assertEquals(
            self.journey,
            Journey.objects.get_current_for_car_user_card(
                self.car, self.user.user_card, datetime.now())
        )


class TestJourneyManager(CarEnabledTestCase):
    def setUp(self):
        Reservation.objects.all().delete()
        super(TestJourneyManager, self).setUp()
        self.journey = None

    def tearDown(self):
        if self.journey is not None:
            self.journey.delete()

    def start_journey(self):
        self.journey = Journey.objects.start_journey(self.car, self.user, datetime.now())

    @raises(AssertionError)
    def test_start_journey_inactive_card(self):
        self.user.user_card.active = False
        self.user.user_card.save()
        self.start_journey()

    @raises(AssertionError)
    def test_start_journey_missing_reservation(self):
        self.user.user_card.is_service_card = False
        self.user.user_card.save()
        self.start_journey()

    def test_start_journey_service_card(self):
        self.user.user_card.is_service_card = True
        self.user.user_card.active = True
        self.user.user_card.save()
        self.start_journey()
        self.assertTrue(isinstance(self.journey, Journey))

    def test_start_journey_with_reservation(self):
        if self.car.get_current_journey() is not None:
            self.car.get_current_journey().delete()

        self.user.user_card.is_service_card = False
        self.user.user_card.active = True
        self.user.user_card.save()

        Reservation.objects.create(
            reserved_from=(datetime.now() - timedelta(minutes=1)),
            reserved_until=(datetime.now() + timedelta(hours=1)),
            car=self.car,
            user=self.user
        )
        self.start_journey()
        self.assertTrue(isinstance(self.journey, Journey))
        self.assertTrue(self.journey.reservation.started != None)


class TestJourneyManagerNormalization(CarEnabledTestCase):
    def setUp(self):
        super(TestJourneyManagerNormalization, self).setUp()
        if self.car.get_current_journey() is not None:
            self.car.get_current_journey().delete()

    @raises(AssertionError)
    def test_reservation_without_journey(self):
        r = Reservation.objects.create(
            reserved_from=datetime(year=2010, month=1, day=1),
            reserved_until=datetime(year=2010, month=1, day=2),
            car=self.car,
            user=self.user
        )
        Journey.objects.normalize_for_reservation(r)

    def test_inactive_addition(self):
        r = Reservation.objects.create(
            reserved_from=datetime(year=2010, month=2, day=1, hour=0),
            reserved_until=datetime(year=2010, month=2, day=2, hour=12),
            car=self.car,
            user=self.user
        )
        Journey.objects.create(
            start_datetime=datetime(year=2010, month=2, day=1, hour=0),
            end_datetime=datetime(year=2010, month=2, day=1, hour=10),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            reservation=r,
        )
        Journey.objects.normalize_for_reservation(r)
        self.assertEquals(len(r.journeys.all()), 2)
        self.assertEquals(r.journeys.order_by('-end_datetime')[0].type,
            Journey.TYPE_WAITING)

    def test_inactive_inside(self):
        r = Reservation.objects.create(
            reserved_from=datetime(year=2010, month=3, day=1, hour=0),
            reserved_until=datetime(year=2010, month=3, day=1, hour=12),
            car=self.car,
            user=self.user
        )
        Journey.objects.create(
            start_datetime=datetime(year=2010, month=3, day=1, hour=0),
            end_datetime=datetime(year=2010, month=3, day=1, hour=5),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            reservation=r,
        )
        Journey.objects.create(
            start_datetime=datetime(year=2010, month=3, day=1, hour=7),
            end_datetime=datetime(year=2010, month=3, day=1, hour=12),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            reservation=r,
        )
        Journey.objects.normalize_for_reservation(r)
        self.assertEquals(len(r.journeys.all()), 3)
        self.assertEquals(r.journeys.order_by('-end_datetime')[1].type,
            Journey.TYPE_WAITING)

    def test_late_return(self):
        r = Reservation.objects.create(
            reserved_from=datetime(year=2010, month=4, day=1, hour=0),
            reserved_until=datetime(year=2010, month=4, day=1, hour=12),
            car=self.car,
            user=self.user
        )
        Journey.objects.create(
            start_datetime=datetime(year=2010, month=4, day=1, hour=0),
            end_datetime=datetime(year=2010, month=4, day=1, hour=18),
            car=self.car,
            user=self.user,
            type=Journey.TYPE_TRIP,
            reservation=r,
        )
        Journey.objects.normalize_for_reservation(r)
        self.assertEquals(len(r.journeys.all()), 2)
        self.assertEquals(r.journeys.order_by('-end_datetime')[0].type,
            Journey.TYPE_LATE_RETURN)
