from datetime import datetime
from functools import partial
from pipetools import where, X, foreach, pipe

from django.conf import settings
from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.db.models.fields import PointField
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import Q
from django.forms import model_to_dict


config = {
    'MODEL': None,
    'SRID': 4326,
}


config.update(settings.GEOTRACK)


LocationField = partial(PointField, srid=config['SRID'])


class LogEntryBase(models.Model):
    """
    Abstract base model for Geotrack log entry.
    """

    # Hard-coding this as an integer field for simplicity for the moment.
    unit_id = models.PositiveIntegerField(db_index=True)

    timestamp = models.DateTimeField(db_index=True,
        help_text='Date/time when the measurement was taken.')
    location = LocationField()
    added = models.DateTimeField(default=datetime.now,
        help_text='When the log entry arrived in the system')

    objects = GeoManager()

    class Meta:
        abstract = True
        ordering = 'timestamp',


class LastKnownPosition(models.Model):
    """
    De-normalization to speed up last position lookups, e.g. where the units
    (most-likely) are 'now'.
    """
    unit_id = models.PositiveIntegerField(unique=True)
    timestamp = models.DateTimeField(db_index=True)
    location = LocationField()
    modified_on = models.DateTimeField(auto_now=True)


try:
    app_label, model_name = config['MODEL'].split('.')
except (AttributeError, ValueError):
    raise ImproperlyConfigured(
        'Please specify GEOTRACK_BACKEND_MODEL in settings in the'
        'following format: "app_label.model_name".')


def get_storage_model():
    storage_model = models.get_model(app_label, model_name)
    if not storage_model:
        raise ImproperlyConfigured(
            'Could not find model "{0}.{1}". Is "{0}" in INSTALLED_APPS?'
            .format(app_label, model_name))
    return storage_model


def store(**kwargs):
    data = dict(kwargs, location=encode_location(kwargs['location']))
    get_storage_model().objects.create(**data)


def query(start=None, end=None, in_polygon=None, units=None):
    return get_storage_model().objects.filter(*([
        start and Q(timestamp__gte=start),
        end and Q(timestamp__lte=end),
        in_polygon and Q(location__within=encode_polygon(in_polygon)),
        units and Q(unit_id__in=units),
    ] > where(X)))


encode_location = pipe | 'POINT({0} {1})'
encode_polygon = foreach('{0} {1}') | ', '.join | 'POLYGON(({0}))'
decode_location = ~X.coords


def transform_entry(instance):
    return dict(model_to_dict(instance, exclude=['id']),
        location=decode_location(instance.location))


transform = foreach(transform_entry) | tuple
