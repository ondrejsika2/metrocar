'''
Created on 25.2.2010

@author: xaralis
'''
from datetime import datetime

from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from metrocar.utils.emails import EmailSender
from metrocar.reservations.models import ReservationError, ReservationReminder
from metrocar.subsidiaries.models import Subsidiary

class ReservationPlugin(object):
    @classmethod
    def post_save(cls, reservation, **kwargs):
        pass
    
    @classmethod
    def pre_save(cls, reservation, **kwargs):
        pass
    
class AddReminderPlugin(ReservationPlugin):
    @classmethod
    def pre_save(cls, reservation, **kwargs):
        """
        If reminder is selected, validation is performed.
        """
        now = datetime.now()
        if kwargs.has_key('with_reminder') and kwargs.has_key('reminder_datetime') and kwargs['with_reminder']:
            
            reminder_datetime = kwargs['reminder_datetime']
            assert isinstance(reminder_datetime, datetime)
            if reminder_datetime <= now:
                raise ReservationError(_('Cannot create reservation reminder '
                    'in the past.'))
            if reminder_datetime > reservation.reserved_from:
                raise ReservationError(_('Cannot create reminder after '
                    'reservation start.'))
        return True
    
    @classmethod
    def post_save(cls, reservation, **kwargs):
        """
        Creates reminder if requested.
        """
        if kwargs.has_key('with_reminder') and kwargs.has_key('reminder_datetime') and kwargs['with_reminder']:
            ReservationReminder.objects.create_for_reservation(reservation,
                kwargs['reminder_datetime'])
            
class SendEmailPlugin(ReservationPlugin):
    @classmethod
    def post_save(cls, reservation, **kwargs):
        """
        Sends e-mail confirming the reservation.
        """
        EmailSender.send_mail( [ reservation.user.email ], 'RES_SUC',reservation.user.language, reservation )
        
