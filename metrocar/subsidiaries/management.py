# encoding: utf-8
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import signals
from django.dispatch import receiver

from metrocar.subsidiaries import models
from metrocar.subsidiaries.models import Subsidiary


@receiver(signals.post_syncdb, sender=models)
def initial_data(sender, **kwargs):

    # create a default Subsidiary if none exist
    if not Subsidiary.objects.exists():
        Subsidiary.objects.create(
            site=Site.objects.get_current(),
            name='Default Subsidiary',
            email=settings.SERVER_EMAIL,
            street='(Please fill in)',
            house_number=1,
            city='(Please fill in)',
        )
