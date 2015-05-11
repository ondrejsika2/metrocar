'''
Created on 23.4.2010

@author: xaralis
'''
from metrocar.user_management.models import Deposit, Account, AccountActivity, MetrocarUser

from test_metrocar.helpers import UserEnabledTestCase

import django.test
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1


class TestAccountActivity(django.test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        MetrocarUser.objects.all().delete()
        Account.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        MetrocarUser.objects.all().delete()

    def setUp(self):
        self.user_1 = create_user_1()

    def tearDown(self):
        MetrocarUser.objects.all().delete()
    
    def test_0_save(self):
        old_account_balance = self.user_1.account.balance
        d = Deposit(account=self.user_1.account, money_amount=300, credited=False)
        d.save()
        a = Account.objects.get(user=self.user_1)
        self.assertEquals(a.balance, old_account_balance + d.money_amount_with_tax)
        self.assertEquals('deposit', d.content_type.model)
        
        d2 = Deposit(account=self.user_1.account, money_amount=300, credited=True)
        d.save()
        a = Account.objects.get(user=self.user_1)
        self.assertEquals(a.balance, old_account_balance + d.money_amount_with_tax)
        
    def test_1_as_concrete_class(self):
        d = Deposit(account=self.user_1.account, money_amount=300, credited=True)
        d.save()
        
        acc_act = AccountActivity.objects.get(pk=d.pk)
        self.assertEquals(acc_act.money_amount, 300)
        self.assertTrue(isinstance(acc_act.as_concrete_class(), Deposit))
