'''
Created on 5.3.2010

@author: xaralis
'''

from django.core.management.base import NoArgsCommand
from datetime import date

from metrocar.user_management.models import MetrocarUser
from metrocar.invoices.models import Invoice

class Command(NoArgsCommand):
    """
    Runs regularly, goes through all users and for each user does this:
	 - Creates invoice if his invoice date is today
     - Generates PDF version
     - Sends those invoices with PDFs to e-mails given.
    """
    
    def handle_noargs(self, **options):
        # first get all users (not just local ones)
        for u in MetrocarUser.objects.all():
            if u.invoice_date.day == date.today().day:
                inv = Invoice.create_invoice(u)
                if inv != None:
                    inv.send_by_email()
				
