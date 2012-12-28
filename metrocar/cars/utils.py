# encoding: utf-8
from datetime import datetime
from pipetools import maybe, foreach, X

from django.conf import settings

from olwidget.widgets import InfoMap, MapDisplay

from metrocar.cars.models import Car, CarModelManufacturer, Fuel, CarType, CarColor, CarModel
from metrocar.subsidiaries.models import Subsidiary


def get_car_infomap(width='100%', height='400px'):
    """
    Returns olwidget.widgets.InfoMap instance with available cars on it.
    """
    return InfoMap([
        [ c.last_position, c.__unicode__() ] for c in Car.objects.all() ],
        options={
            'default_zoom': 8,
            'map_div_style': {'width': width, 'height': height},
            'popupOutside': True,
            'overlayStyle': {
                'externalGraphic': settings.STATIC_URL + "img/marker.png",
                'backgroundGraphic': settings.STATIC_URL + "img/marker_shadow.png",
                'graphicXOffset': -10,
                'graphicYOffset': -12,
                'graphicWidth': 21,
                'graphicHeight': 25,
                'backgroundXOffset': 2,
                'graphicOpacity': 1
            }
        }
    )


def get_map_for_geometry(geometry, width, height):
    """
    Returns basic MapDisplay instance for any GEOS geometry.
    """
    return MapDisplay(
        fields=[ geometry ],
        options={
            'default_zoom': 11,
            'map_div_style': {'width': width, 'height': height}
         }
    )


# TODO: smarter grouping....

def get_grouping_precision(bounds):
    x_min = min(x for (x, y) in bounds)
    x_max = max(x for (x, y) in bounds)
    dx = x_max - x_min
    return (
        20 if dx < .12 else
        2 if dx < .5 else
        1 if dx < 1.5 else
        0)


def grouping_precision(location, bounds=None, default=2):
    """
    Limit `location` precision to a level suitable for grouping locations
    for a view of given bounds (polygon). If no bounds given `default`
    precision will be used.
    """
    precision = get_grouping_precision(bounds) if bounds else default
    return tuple((round((n * 5), precision) / 5) for n in location)


# model factories:

def manufacturer(slug, name=None):
    return CarModelManufacturer.objects.get_or_create(
        slug=slug, defaults={'name': slug.capitalize()})[0]


def fuel(title):
    return Fuel.objects.get_or_create(title=title)[0]


def car_type(type):
    return CarType.objects.get_or_create(type=type)[0]


def color(color):
    return CarColor.objects.get_or_create(color=color)[0]


def car_model(make, name, **kwargs):
    defaults = dict(
        type=car_type('Hatchback'),
        engine='(unknown)',
        seats_count=5,
        storage_capacity=200,
        main_fuel=fuel('Natural'),
    )
    defaults.update(kwargs)
    return CarModel.objects.get_or_create(
        name=name,
        manufacturer=make,
        defaults=defaults,
    )[0]


def car(model, registration_number, **kwargs):
    defaults = dict(
        active=True,
        manufacture_date=datetime(2000, 1, 1),
        color=color(u'Šedá'),
        home_subsidiary=Subsidiary.objects.get_current(),
    )
    defaults.update(**kwargs)
    return Car.objects.get_or_create(
        model=model,
        registration_number=registration_number,
        defaults=defaults,
    )[0]
