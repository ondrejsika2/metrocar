'''
Created on 7.5.2010

@author: xaralis
'''
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ImproperlyConfigured

class PricelistManager(models.Manager):
    def valid(self):
        """
        Returns only pricelists which are valid and available at the moment.
        """
        return self.get_query_set().filter(deleted=False, available=True)
    
class PricelistDayManager(models.Manager):
    def weekdays(self):
        """
        Returns only weekday records order by weekday succession
        """
        return self.get_query_set().filter(date__isnull=True,
            weekday_from__isnull=False).order_by('weekday_from')
    
    def dates(self):
        """
        Returns only date record order by their date
        """
        return self.get_query_set().filter(date__isnull=False,
            weekday_from__isnull=True).order_by('date')
            
class StornoFeeManager(models.Manager):
    @classmethod
    def get_record_for_reservation(self, reservation, now=datetime.now()):
        """
        Searches for right StornoFeeTimeline record by comaring time duration 
        till reservation start
        """
        from metrocar.reservations.models import Reservation
        from metrocar.tarification.models import StornoFeeTimeline
        assert isinstance(reservation, Reservation)
        assert isinstance(now, datetime)
        difference = reservation.reserved_from - now
        try:
            timeline_rec = StornoFeeTimeline.objects.filter(
                preceeding_time_from__lte=difference.seconds
            ).order_by('-preceeding_time_from')[0]
            return timeline_rec
        except IndexError, e:
            if len(StornoFeeTimeline.objects.all()) != 0:
                raise AssertionError(_('Too late to cancel the reservation.'))
            raise ImproperlyConfigured(_('No storno fee record found.'))
    
    def create_for_reservation(self, reservation):
        """
        Generates new StornoFee for reservation (used when it's cancelled)
        """
        from metrocar.reservations.models import Reservation
        assert isinstance(reservation, Reservation)
        if reservation.finished:
            raise AssertionError(_('Trying to cancel already finished '
                'reservation'))
        timeline_rec = self.get_record_for_reservation(reservation)
        fee = self.model(
             reservation=reservation,
             fee_timeline=timeline_rec,
             money_ammount=timeline_rec,
             account=reservation.user.account
        )
        fee.save()
        return fee
