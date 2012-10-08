# encoding: utf-8
from metrocar.cars.utils import manufacturer, car_type, fuel, color, car
from metrocar.cars.utils import car_model


def create():

    s120 = car_model(manufacturer('skoda'), '120L',
        type=car_type('Sedan'),
        main_fuel=fuel('Special'),
    )
    favo = car_model(manufacturer('skoda'), 'Favorit')
    zetor = car_model(manufacturer('zetor'), '3.0T',
        seats_count=1,
        main_fuel=fuel('diesel'),
        type=car_type('Traktor'),
    )

    return {
        'car_models': [s120, favo, zetor],
        'cars': [
            car(s120, 'S-120-L'),
            car(s120, 'S-120-R', color=color(u'Rezavá')),
            car(favo, 'FAVO-1', color=color(u'Bílá')),
            car(zetor, 'ZETOR', color=color(u'Modrá')),
        ],
    }
