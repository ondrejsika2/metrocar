'''
Created on 7.5.2010

@author: xaralis
'''
from django.db import models

class InvoiceItemManager(models.Manager):
    def create_for_invoice(self, sender, **kwargs):
        """
        Creates invoice items for an invoice. Invoice items are all uninvoiced
        account activities for invoice user.
        """
        from metrocar.invoices.models import Invoice
        if not kwargs['created']: return
        invoice = kwargs['instance']
        assert isinstance(invoice, Invoice)
        univoiced_activities = invoice.user.get_invoiceable_activities()
        items = []
        for activity in univoiced_activities:
            i = self.model(invoice=invoice, account_activity=activity)
            i.save()
            items.append(i)
        return items
