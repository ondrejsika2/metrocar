from functools import partial
from pipetools import maybe

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from metrocar.cars.models import Car
from geotrack.backends.geodjango.models import LogEntryBase


generate_key = partial(get_random_string, 50,
    'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')


class CarUnit(models.Model):

    unit_id = models.PositiveIntegerField(unique=True, help_text=_(
        'A unique identifier for this unit for the API and Geotrack'))

    secret_key = models.CharField(default=generate_key, help_text=_(
        'A secret key for accessing the API from the unit.'), max_length=50)

    car = models.ForeignKey(Car, null=True, blank=True, help_text=_(
        'A car in which this unit is currently installed'))

    enabled = models.BooleanField(default=True, help_text=_(
        'If disabled, the unit will be denied access to the API.'))

    class Meta:
        verbose_name = _('Car unit')
        verbose_name_plural = _('Car units')

    def __unicode__(self):
        return u'{0} ({1})'.format(
            self.unit_id, self.car > maybe | 'in {0}' or 'unassigned')


class LogEntry(LogEntryBase):
    event = models.CharField(max_length=30, db_index=True,
        null=True, blank=True)
