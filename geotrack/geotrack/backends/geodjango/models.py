from datetime import datetime
from functools import partial

from django.conf import settings
from django.contrib.gis.db.models import GeoManager
from django.contrib.gis.db.models.fields import PointField
from django.core.exceptions import ImproperlyConfigured
from django.db import models


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

    def save(self, **kwargs):
        super(LogEntryBase, self).save(**kwargs)
        self.update_last_known_position()

    def update_last_known_position(self):
        data = dict(timestamp=self.timestamp, location=self.location)

        last_pos, created = LastKnownPosition.objects.get_or_create(
            unit_id=self.unit_id, defaults=data)

        if not created and last_pos.timestamp < self.timestamp:
            for name, val in data.items():
                setattr(last_pos, name, val)
            last_pos.save()


class LastKnownPosition(models.Model):
    """
    De-normalization to speed up last position lookups.
    """
    unit_id = models.PositiveIntegerField(unique=True)
    timestamp = models.DateTimeField(db_index=True)
    location = LocationField()
    modified_on = models.DateTimeField(auto_now=True)

    objects = GeoManager()


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
