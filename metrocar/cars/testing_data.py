# encoding: utf-8
from metrocar.cars.utils import manufacturer, car_type, fuel, color, car
from metrocar.cars.utils import car_model


def create():

    hyundai = car_model(manufacturer('hyundai'), 'Vagon', engine='1.2TDi')

    fabia = car_model(manufacturer('skoda', u'Škoda'), 'Fabia',
        engine='1.6 TDI CR 77 kW')

    octavia = car_model(manufacturer('skoda'), 'Octavia',
        type=car_type('Sedan'),
        engine='1.4 59 kW',
        main_fuel=fuel('diesel'))

    focus = car_model(manufacturer('ford'), 'Focus',
        type=car_type('Combi'),
        engine='1.6 Ti-VCT 77kW')

    return {
        'car_models': [hyundai, fabia, octavia, focus],
        'cars': [
            car(hyundai, '1A1 3045', color=color(u'Zelená')),
            car(hyundai, '1A1 1708', color=color(u'Bílá')),
            car(fabia, '2AL 4089', color=color(u'Modrá')),
            car(fabia, '1A3 7805', color=color(u'Černá')),
            car(octavia, '3A4 3134', color=color(u'Bílá')),
            car(octavia, '6A4 6634', color=color(u'Bílá')),
            car(octavia, '1A0 7004', color=color(u'Červená')),
            car(focus, '7A8 9402', color=color(u'Modrá')),
        ],
    }
