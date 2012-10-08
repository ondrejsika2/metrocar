# encoding: utf-8
from pipetools import as_args

from django.dispatch import receiver
from django.db.models import signals

from metrocar.cars import models
from metrocar.cars.utils import manufacturer, car_type, fuel_type, color


@receiver(signals.post_syncdb, sender=models)
def initial_data(sender, **kwargs):

    map(as_args(manufacturer), [
        ('Hyundai', 'hyundai'),
        ('Ford', 'ford'),
        (u'Škoda', 'skoda'),
    ])

    map(fuel_type, ['Natural', 'Diesel'])

    map(car_type, ['Hatchback', 'Sedan', 'Coupe'])

    map(color, [u'Černá', u'Bílá'])
