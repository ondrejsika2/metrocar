from random import randint, random
from geotrack import dummy_generator

from metrocar.car_unit_api import testing_data as car_units_testing_data


def create():
    units = car_units_testing_data.create()['car_units']

    for u in units:
        create_random_geo_data(u.unit_id)


def extra_data_generator():
    v = randint(0, 180)  # kph
    fuel = random() * 40 + 5  # liters
    odometer = randint(10000, 300000)  # km
    while True:
        dv = random() * 50 - 25  # kph
        v = min(180, v + dv) + random() * 5
        consumption = max(random(), random() * (dv / 3.0)) + 5
        fuel -= (random() * 0.1 + 0.1)
        if fuel < (random() * 5 + 2):
            fuel = random() * 30 + 20
        odometer += random()
        yield {
            'velocity': v,
            'fuel_remaining': fuel,
            'consumption': consumption,
        }


def create_random_geo_data(unit_id):
    extra_data = extra_data_generator()

    dummy_generator.create_and_store_dummy_route(
        unit_id=unit_id,
        get_extra_data=lambda location, index: extra_data.next(),
    )
