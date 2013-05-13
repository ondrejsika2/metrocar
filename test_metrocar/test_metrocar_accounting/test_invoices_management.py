from metrocar.user_management.models import Deposit, Account, MetrocarUser
from metrocar.accounting import invoices_management
from decimal import Decimal
from metrocar.invoices.models import Invoice
from helpers import UserEnabledTestCase
import re

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

    def test_0_create_inv(self):
        #create invoice in accounting system
        invoices_management.create_invoice(self.invoice)
        inv = invoices_management.get_invoice(self.invoice)
        assert inv != None
        assert Decimal(str(inv['sumCelkem'])) == self.invoice.total_price_with_tax()
        #flexibee adds zeors to the varSym
        varSym = str(inv['varSym'])
        #remove leading zeros
        varSym = re.sub("^0+","",varSym)
        assert varSym == str(self.invoice.variable_symbol)

    def tearDown(self):
        super(TestInvoicesManagement, self).tearDown()
        self.invoice.delete()
        self.dep1.delete()
        self.dep2.delete()
