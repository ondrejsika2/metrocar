from datetime import datetime, timedelta
from metrocar.reservations.models import Reservation
from metrocar.cars import testing_data as cars_testing_data
from metrocar.user_management import testing_data as users_testing_data

cars = cars_testing_data.create()['cars']
users = users_testing_data.create()['users']

def create_reservation_1(save=True):
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(hours=1)),
        reserved_until=(datetime.now() + timedelta(hours=12)),
        user=users[1],
        car=cars[0]
    )[0]


def create_reservation_2(save=True):
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(hours=13)),
        reserved_until=(datetime.now() + timedelta(hours=22)),
        user=users[1],
        car=cars[1],
        cancelled=True
    )[0]


def create():
    return {
        'reservations': [
            create_reservation_1(),
            create_reservation_2(),
        ]
    }