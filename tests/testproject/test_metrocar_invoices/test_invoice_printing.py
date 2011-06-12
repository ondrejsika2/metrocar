'''
Created on 23.4.2010

@author: xaralis
'''
from nose.tools import raises

from django.core.urlresolvers import reverse
from django.http import HttpResponse

from metrocar.invoices.printing import PrintableInvoice, PrintableInvoicePdf

from testproject.test_metrocar_invoices import InvoiceEnabledTestCase

class TestPrint(InvoiceEnabledTestCase):
    def test_0_get_printable_invoice(self):
        self.assert_true(isinstance(self.invoice.get_printable_invoice(),
            PrintableInvoice))
    
    @raises(ValueError)
    def test_1_get_printable_invoice_nonexistent_format(self):
        self.assert_true(isinstance(self.invoice.get_printable_invoice(
            format='neexistujici-format'), PrintableInvoice))
        
    def test_2_get_content(self):
        pinv = self.invoice.get_printable_invoice()
        self.assert_true(isinstance(pinv, PrintableInvoicePdf))
        self.assert_equals(pinv.get_mime(), 'application/pdf')
        self.assert_true(isinstance(pinv.get_response(), HttpResponse))
    
    def test_3_printing_view_not_logged_in(self):
        resp = self.client.get(reverse('metrocar_invoices_print', kwargs={'invoice_id': self.invoice.id}))
        self.assert_equals(403, resp.status_code)
        
    def test_4_printing_view_logged_in(self):
        self.client.login(username=self.user.username, password='testpass')
        resp = self.client.get(reverse('metrocar_invoices_print', kwargs={'invoice_id': self.invoice.id}))
        self.assert_equals(200, resp.status_code)
        