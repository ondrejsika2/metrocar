'''
Created on 23.4.2010

@author: xaralis
'''

from metrocar.invoices.models import Invoice

from tests.testproject.test_metrocar_invoices import InvoiceEnabledTestCase

class Test(InvoiceEnabledTestCase):
    def test_create_vs(self):
        self.assert_true(isinstance(Invoice.create_vs(), unicode))
    
    def test_invoice_save(self):
        self.assert_true(self.invoice.variable_symbol is not None)
        self.assert_true(self.invoice.draw_date is not None)
        self.assert_true(self.invoice.due_date is not None)