from django.db import models

from geotrack.backends.geodjango.models import LogEntryBase


class GeoLogEntry(LogEntryBase):
    custom_field = models.IntegerField()
