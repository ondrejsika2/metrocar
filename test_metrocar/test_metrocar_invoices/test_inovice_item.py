'''
Created on 23.4.2010

@author: xaralis
'''
from test_metrocar.test_metrocar_invoices import InvoiceEnabledTestCase

class TestInvoiceItem(InvoiceEnabledTestCase):
    def test_0_create_for_invoice(self):
        # self.acc_act_3 was already credited
        self.assert_equals(len(self.invoice.items.all()), 2)

    def test_1_amount(self):
        ii = self.invoice.items.all()[0]
        self.assert_equals(ii.amount,
            self.acc_act_1.money_amount)


