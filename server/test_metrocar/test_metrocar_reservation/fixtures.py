from datetime import datetime, timedelta
from metrocar.cars.managers import JourneyManager
from metrocar.reservations.models import Reservation, ReservationBill
from test_metrocar.test_metrocar_cars.fixtures import create_car_1
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1
from metrocar.user_management.models import UserCard


def create_reservation_1():
    reservation = Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(hours=1)),
        reserved_until=(datetime.now() + timedelta(hours=12)),
        user=create_user_1(),
        car=create_car_1(),
        price=120,
    )[0]

    journey = JourneyManager()
    journey.create_complete_journey(
        car = reservation.car,
        user_card=reservation.user,
        datetime_since=reservation.reserved_from,
        datetime_till=reservation.reserved_until,
    )

    ReservationBill.objects.create_for_reservation(reservation)

    return reservation


def create_reservation_2():
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(hours=13)),
        reserved_until=(datetime.now() + timedelta(hours=22)),
        user=create_user_1(),
        car=create_car_1()
    )[0]
