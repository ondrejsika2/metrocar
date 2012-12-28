from decimal import Decimal
from functools import partial
from pipetools import maybe, unless

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from geotrack.api import query

from metrocar.cars.models import Car


class Events:
    """
    Possible values of LogEntry.event
    """
    UNLOCKED = 'UNLOCKED'
    LOCKED = 'LOCKED'
    ENGINE_ON = 'ENGINE_ON'
    ENGINE_OFF = 'ENGINE_OFF'


generate_key = partial(get_random_string, 50,
    'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')


class CarUnitManager(models.Manager):

    def get_for(self, car):
        """
        Returns a CarUnit installed in `car` or None if no such unit exists.

        Raises an exception if there are more CarUnits in the `car`, but that
        probably shouldn't happen.
        """
        return unless(CarUnit.DoesNotExist, self.get_query_set().get)(car=car)


class CarUnit(models.Model):
    """
    A model representing a car unit that will report car location and status
    through the car-unit API.
    """

    unit_id = models.PositiveIntegerField(unique=True, help_text=_(
        'A unique identifier for this unit for the API and Geotrack'))

    secret_key = models.CharField(default=generate_key, help_text=_(
        'A secret key for accessing the API from the unit.'), max_length=50)

    car = models.ForeignKey(Car, null=True, blank=True, help_text=_(
        'A car in which this unit is currently installed'))

    enabled = models.BooleanField(default=True, help_text=_(
        'If disabled, the unit will be denied access to the API.'))

    objects = CarUnitManager()

    class Meta:
        verbose_name = _('Car unit')
        verbose_name_plural = _('Car units')

    def __unicode__(self):
        return u'{0} ({1})'.format(
            self.unit_id, self.car > maybe | 'in {0}' or 'unassigned')

    def get_last_position(self):
        return query('last_position', units=[self.unit_id]).get(self.unit_id)


if settings.GEO_ENABLED:

    from geotrack.backends.geodjango.models import LogEntryBase

    class LogEntry(LogEntryBase):
        """
        A model for storing logs from car units in Geotrack.
        """
        event = models.CharField(max_length=30, db_index=True,
            null=True, blank=True)

        user_id = models.IntegerField(null=True, blank=True, db_index=True)
        odometer = models.DecimalField(decimal_places=2, max_digits=8,
            null=True, blank=True)
        velocity = models.FloatField(null=True, blank=True)
        consumption = models.FloatField(null=True, blank=True)
        fuel_remaining = models.FloatField(null=True, blank=True)
        altitude = models.FloatField(null=True, blank=True)
        engine_temp = models.FloatField(null=True, blank=True)
        engine_rpm = models.FloatField(null=True, blank=True)
        throttle = models.FloatField(null=True, blank=True)

        def save(self, *args, **kwargs):
            # odometer value could be float, which would cause an error, so...
            self.odometer = self.odometer > maybe | str | Decimal
            super(LogEntry, self).save(*args, **kwargs)
