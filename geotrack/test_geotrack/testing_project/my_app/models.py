from django.db import models

from geotrack.backends.geodjango import LogEntryBase


class GeoLogEntry(LogEntryBase):
    custom_field = models.IntegerField()
