from pipetools import maybe, X

from django.conf import settings

if settings.GEO_ENABLED:
    from django.contrib.gis.db.models import GeoManager
else:
    from django.db.models import Manager as GeoManager


def get_car_last_position(car):
    """
    Returns car's last known position.

    First attempts to get it from a CarUnit assigned to `car` and if that fails
    (no CarUnit or it doesn't know the position) it falls back to the car's
    last_position attribute, which might have been filled out manually.
    """
    from metrocar.car_unit_api.models import CarUnit
    from_car_unit = CarUnit.objects.get_for(car) > maybe | X.get_last_position()
    return from_car_unit or car.last_position
