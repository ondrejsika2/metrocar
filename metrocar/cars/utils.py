from django.conf import settings
from django.template.defaultfilters import slugify

from olwidget.widgets import InfoMap, MapDisplay

from models import Car, CarModelManufacturer, Fuel, CarType, CarColor


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


# model factories:

def manufacturer(name, slug=None):
    return CarModelManufacturer.objects.get_or_create(
        slug=(slug or slugify(name)), defaults={'name': name})


def fuel_type(title):
    return Fuel.objects.get_or_create(title=title)


def car_type(type):
    return CarType.objects.get_or_create(type=type)


def color(color):
    return CarColor.objects.get_or_create(color=color)
