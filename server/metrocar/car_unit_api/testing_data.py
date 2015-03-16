from metrocar.car_unit_api.models import CarUnit
from metrocar.cars import testing_data as cars_testing_data


def unit(unit_id, car=None, **kwargs):
    return CarUnit.objects.get_or_create(unit_id=unit_id, car=car, **kwargs)[0]


def create():
    cars = cars_testing_data.create()['cars']
    return {
        'car_units': [
            unit(123, cars[0]),
            unit(456, cars[1]),
            unit(789, cars[2]),
            unit(147, cars[3]),
            unit(258, cars[4]),
            unit(369, cars[5]),
            unit(753, cars[6]),
            unit(951, cars[7]),
        ]
    }
