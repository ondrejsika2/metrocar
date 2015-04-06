# encoding: utf-8

from metrocar.cars.utils import car_model, car_type, fuel, color, car, fuel_bill_1, fuel_bill_2, fuel_bill_3, \
    manufacturer, parking_1, parking_2, parking_3, parking_4
from metrocar.user_management import testing_data as users_testing_data
from metrocar.user_management.testing_data import get_account

users = users_testing_data.create()['users']

def create():

    hyundai = car_model(manufacturer('hyundai'), 'Hyundai i20', engine='1.2TDi')

    fabia = car_model(manufacturer('skoda', u'Škoda'), 'Škoda Fabia',
        engine='1.6 TDI CR 77 kW')

    octavia = car_model(manufacturer('skoda'), 'Škoda Octavia',
        type=car_type('Sedan'),
        engine='1.4 59 kW',
        main_fuel=fuel('diesel'))

    focus = car_model(manufacturer('ford'), 'Ford Focus',
        type=car_type('Combi'),
        engine='1.6 Ti-VCT 77kW')

    car_parking_1 = parking_1()
    car_parking_2 = parking_2()
    car_parking_3 = parking_3()
    car_parking_4 = parking_4()

    car_hyundai_1 = car(hyundai, '1A1 3045', color=color(u'Zelená'), parking=car_parking_1)
    car_fabia_1 = car(fabia, '2AL 4089', color=color(u'Modrá'), parking=car_parking_2)
    car_octavia_1 = car(octavia, '1A0 7004', color=color(u'Červená'), parking=car_parking_3)
    car_hyundai_2 = car(hyundai, '1A1 1708', color=color(u'Bílá'), parking=car_parking_4)
    car_octavia_2 = car(octavia, '3A4 3134', color=color(u'Černá'), parking=car_parking_1)
    car_focus_1 = car(focus, '7A8 9402', color=color(u'Modrá'), parking=car_parking_2)
    car_octavia_3 = car(octavia, '6A4 6634', color=color(u'Bílá'), parking=car_parking_3)
    car_fabia_2 = car(fabia, '1A3 7805', color=color(u'Černá'), parking=car_parking_2)

    return {
        'car_models': [hyundai, fabia, octavia, focus],
        'cars': [
            car_hyundai_1,
            car_fabia_1,
            car_octavia_1,
            car_hyundai_2,
            car_octavia_2,
            car_focus_1,
            car_octavia_3,
            car_fabia_2
        ],
        'fuel_bills': [
            fuel_bill_1(
                account=get_account(users[1].username),
                car=car_octavia_1,
                fuel=fuel('diesel')
            ),
            fuel_bill_2(
                account=get_account(users[1].username),
                car=car_octavia_1,
                fuel=fuel('diesel')
            ),
            fuel_bill_3(
                account=get_account(users[1].username),
                car=car_octavia_1,
                fuel=fuel('diesel')
            ),
        ],
        'parking': [
            car_parking_1,
            car_parking_2,
            car_parking_3,
            car_parking_4,
        ]
    }
