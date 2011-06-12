'''
Created on 5.3.2010

@author: xaralis
'''

from django.core.management.base import NoArgsCommand
from metrocar.reservations.models import Reservation

class Command(NoArgsCommand):
    """
    Collects reservations which are to be finished and tries to finish them.
    """
    
    def handle_noargs(self, **options):
        # collect reservations and finish them
        for r in Reservation.objects.to_be_finished():
            msg = "Finishing reservation %s ... \t\t %s"
            if r.finish(r.reserved_until, True):
                print msg % (r, 'SUCCESS')
            else:
                print msg % (r, 'FAILURE')
