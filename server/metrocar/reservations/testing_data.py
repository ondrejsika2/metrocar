from datetime import datetime, timedelta
from metrocar.cars.managers import JourneyManager
from metrocar.reservations.models import Reservation, ReservationBill
from metrocar.cars import testing_data as cars_testing_data
from metrocar.user_management import testing_data as users_testing_data

cars = cars_testing_data.create()['cars']
users = users_testing_data.create()['users']

def create_reservation_1(save=True):
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(days=15, hours=1)),
        reserved_until=(datetime.now() + timedelta(days=15, hours=12)),
        user=users[1],
        car=cars[0]
    )[0]


def create_reservation_2(save=True):
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(days=5, hours=13)),
        reserved_until=(datetime.now() + timedelta(days=5, hours=22)),
        user=users[1],
        car=cars[1],
        cancelled=True
    )[0]


def create_reservation_3(save=True):
    reservation = Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(days=-3, hours=13)),
        reserved_until=(datetime.now() + timedelta(days=-3, hours=22)),
        user=users[1],
        car=cars[2],
        price=540,
    )[0]

    journey = JourneyManager()
    journey.create_complete_journey(
        car = reservation.car,
        user_card=reservation.user,
        datetime_since=reservation.reserved_from,
        datetime_till=reservation.reserved_until,
    )

    reservation_bill = ReservationBill.objects.create_for_reservation(reservation)
    reservation_bill.datetime = datetime.now() + timedelta(days=-3, hours=22)
    reservation_bill.save()

    reservation.finished = True
    reservation.save()

    return reservation


def create_reservation_4(save=True):
    reservation = Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(days=-10, hours=3, minutes=40)),
        reserved_until=(datetime.now() + timedelta(days=-10, hours=8, minutes=40)),
        user=users[1],
        car=cars[3],
        price=120,
    )[0]

    journey = JourneyManager()
    journey.create_complete_journey(
        car = reservation.car,
        user_card=reservation.user,
        datetime_since=reservation.reserved_from,
        datetime_till=reservation.reserved_until,
    )

    reservation_bill = ReservationBill.objects.create_for_reservation(reservation)
    reservation_bill.datetime = datetime.now() + timedelta(days=-10, hours=3, minutes=40)
    reservation_bill.save()

    reservation.finished = True
    reservation.save()

    return reservation


def create_reservation_5(save=True):
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(days=-15, hours=13, minutes=15)),
        reserved_until=(datetime.now() + timedelta(days=-15, hours=22, minutes=30)),
        user=users[1],
        car=cars[4],
        cancelled=True
    )[0]


def create_reservation_6(save=True):
    reservation = Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(days=-45, hours=7, minutes=30)),
        reserved_until=(datetime.now() + timedelta(days=-45, hours=21, minutes=45)),
        user=users[1],
        car=cars[5],
        price=760,
    )[0]

    journey = JourneyManager()
    journey.create_complete_journey(
        car = reservation.car,
        user_card=reservation.user,
        datetime_since=reservation.reserved_from,
        datetime_till=reservation.reserved_until,
    )

    reservation_bill = ReservationBill.objects.create_for_reservation(reservation)
    reservation_bill.datetime = datetime.now() + timedelta(days=-45, hours=7, minutes=30)
    reservation_bill.save()

    reservation.finished = True
    reservation.save()

    return reservation

def create():
    return {
        'reservations': [
            create_reservation_1(),
            create_reservation_2(),
            create_reservation_3(),
            create_reservation_4(),
            create_reservation_5(),
            create_reservation_6(),
        ]
    }