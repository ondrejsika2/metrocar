# -*- coding: utf-8 -*-

from metrocar.user_management.models import Deposit, Account, MetrocarUser
from metrocar.accounting import flexibee_accounting
from decimal import Decimal
from metrocar.invoices.models import Invoice
from helpers import UserEnabledTestCase
from datetime import date
import re
from flexipy import config
import flexipy 

class TestInvoicesManagement(UserEnabledTestCase):
    """
    These test should be executed only if ACCOUNTING_ENABLED is True.
    Also if metrocar is now powered by different accounting system then Flexibee 
    these tests should be updated so they reflect current situation.
    """
    def setUp(self):
        super(TestInvoicesManagement, self).setUp()
        #create some deposit into user's account        
        user_account = Account.objects.get(user=self.user)
        self.dep1 = Deposit(money_amount=Decimal('7500'),account=user_account)
        self.dep1.save()
        self.dep2 = Deposit(money_amount=Decimal('6000'),account=user_account)
        self.dep2.save()
        #now create invoice in db
        self.invoice = Invoice.objects.create(user=self.user)
        #create Faktura instance with testing configuration
        testing_conf = config.TestingConfig()
        #create instance of Faktura from flexipy
        faktura = flexipy.Faktura(testing_conf)
        self.bank = flexipy.Banka(testing_conf)
        self.flexManager = flexibee_accounting.FlexibeeManager(faktura)

    def test_0_create_inv(self):
        #create invoice in accounting system
        self.flexManager.create_invoice(self.invoice)
        #get created invoice from accounting system
        inv = self.flexManager.get_invoice(self.invoice)
        assert inv != None
        assert Decimal(str(inv['sumCelkem'])) == self.invoice.total_price_with_tax()
        #flexibee adds zeors to the varSym
        varSym = str(inv['varSym'])
        #remove leading zeros
        varSym = re.sub("^0+","",varSym)
        #assert varSym == str(self.invoice.variable_symbol)

    # def test_1_pair_payments(self):
    #     TODO: there is problem in FLexibee with deleting invoices that are paid
    #     therefore test fails. Undoing of pairing so far is not possible through REST API and flexipy.
    #     It must be done manually through the web interface of Flexibee
    #     #test ability to pair payments and automatically 
    #     #mark invoices as paid
    #     #create bank item
    #     self.flexManager.create_invoice(self.invoice)
    #     today = str(date.today())
    #     dalsiParam = {'sumZklZakl':str(self.invoice.total_price_with_tax()), 'varSym':self.invoice.variable_symbol, 'bezPolozek':True,'typUcOp':u'code:PŘEVOD PENĚZ'}
    #     self.bank.create_bank_doklad(kod='bank15', datum_vyst=today, dalsi_param=dalsiParam)
    #     self.flexManager.check_incoming_payments()
    #     assert self.invoice.status == 'PAID'

    def tearDown(self):
        super(TestInvoicesManagement, self).tearDown()
        self.flexManager.delete_invoice(self.invoice)
        self.invoice.delete()
        self.dep1.delete()
        self.dep2.delete()
