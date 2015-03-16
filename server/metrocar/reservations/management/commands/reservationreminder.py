'''
Created on 5.3.2010

@author: xaralis
'''

from django.core.management.base import NoArgsCommand
from metrocar.reservations.models import ReservationReminder

class Command(NoArgsCommand):
    """
    Sends reservation reminders which are to be send for reservations.
    """
    
    def handle_noargs(self, **options):
        # collect reservations and finish them
        for r in ReservationReminder.objects.ready_to_send():
            msg = "Sending reminder for reservation %s ..." % r.reservation
            r.send()