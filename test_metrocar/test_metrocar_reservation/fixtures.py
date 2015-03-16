from datetime import datetime, timedelta
from metrocar.reservations.models import Reservation
from test_metrocar.test_metrocar_cars.fixtures import create_car_1
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1


def create_reservation_1(save=True):
    reservation = Reservation(
        reserved_from=(datetime.now() + timedelta(hours=1)),
        reserved_until=(datetime.now() + timedelta(hours=12)),
        user=create_user_1(),
        car=create_car_1()
    )
    if save:
        reservation.save()
    return reservation


def create_reservation_2(save=True):
    reservation = Reservation(
        reserved_from=(datetime.now() + timedelta(hours=13)),
        reserved_until=(datetime.now() + timedelta(hours=22)),
        user=create_user_1(),
        car=create_car_1()
    )
    if save:
        reservation.save()
    return reservation