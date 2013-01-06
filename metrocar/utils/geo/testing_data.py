# encoding: utf-8
from csv import DictReader
from datetime import datetime
from itertools import chain, count, izip
from pipetools import pipe, foreach, VALUE, where, maybe, unless, where_not, X
from random import randint, random

from geotrack import dummy_generator

from metrocar.car_unit_api import testing_data as car_units_testing_data
from metrocar.car_unit_api.models import CarUnit
from metrocar.car_unit_api.testing_data import unit
from metrocar.car_unit_api.views import store
from metrocar.cars.models import Car


def create():
    units = car_units_testing_data.create()['car_units']

    assing_positions(units)
    # for u in units:
    #     create_random_geo_data(u.unit_id)


def create_units():
    "Creates CarUnits for existing Cars that don't have them"
    cars_with_units = CarUnit.objects.values_list('car_id', flat=True)
    taken_unit_ids = set(CarUnit.objects.values_list('unit_id', flat=True))
    free_unit_ids = count(1) > where_not(X._in_(taken_unit_ids))
    cars_without_units = Car.objects.all() > where_not(X.id._in_(cars_with_units))
    for car, unit_id in izip(cars_without_units, free_unit_ids):
        unit(unit_id, car)


def extra_data_generator():
    v = randint(0, 180)  # kph
    fuel = random() * 40 + 5  # liters
    odometer = randint(10000, 300000)  # km
    while True:
        dv = random() * 50 - 25  # kph
        v = abs(min(180, v + dv) + random() * 5)
        consumption = max(random(), random() * (dv / 3.0)) + 5
        fuel -= (random() * 0.1 + 0.1)
        if fuel < (random() * 5 + 2):
            fuel = random() * 30 + 20
        odometer += random()
        yield {
            'velocity': v,
            'fuel_remaining': fuel,
            'consumption': consumption,
            'odometer': odometer,
        }


def create_random_geo_data(unit_id):
    extra_data = extra_data_generator()

    dummy_generator.create_and_store_dummy_route(
        unit_id=unit_id,
        get_extra_data=lambda location, index: extra_data.next(),
    )


def position_generator():
    p = [
        (14.41668, 50.07644),
        (14.45385, 50.07739),
        (14.39248, 50.10206),
        (14.41665, 50.07654),
        (14.38855, 50.10294),
        (14.39029, 50.10528),
        (14.42082, 50.07609),
        (14.42659, 50.10076),
        (14.42434, 50.06766),
    ]

    def random():
        while True:
            yield dummy_generator.random_point(
                ((14.36325, 14.57268), (49.99847, 50.12916)))

    return chain(p, random())


def assing_positions(units):
    g = position_generator()
    for u in units:
        entry = dict(location=g.next(), timestamp=datetime.now())
        store(u.unit_id, [entry])


def entry_from_torque(data):
    """
    Convert an item from Torque-app [1] CSV to a valid Geotrack entry.

    TODO: convert timestamp, just did it manually in the csv for now...

    [1] http://torque-bhp.com/
    """
    cleaned_data = dict((k.strip(), v) for k, v in data.iteritems())

    get = lambda T, k: k > maybe | cleaned_data.get | unless(ValueError, T)

    return (
        ('altitude',
            get(float, 'Altitude')),
        ('consumption',
            get(float, 'Fuel flow rate/hour(l/hr)')),
        ('engine_temp',
            get(float, 'Engine Coolant Temperature(C)')),
        ('engine_rpm',
            get(float, 'Engine RPM(rpm)')),
        ('fuel_remaining',
            get(float, 'Fuel Remaining (Calculated from vehicle profile)(%)')),
        ('location', (
            get(float, 'Longitude'), get(float, 'Latitude'))),
        ('throttle',
            get(float, 'Absolute Throttle Position B(%)')),
        ('timestamp',
            get(str, 'GPS Time')),
        ('velocity',
            (get(float, 'GPS Speed (Meters/second)') or 0) * 3.6),
    ) > where(VALUE) | dict


def import_csv(unit_id, filename, make_entry):
    (filename > pipe
        | open
        | DictReader
        | foreach(make_entry)
        | tuple
        | (store, unit_id))
