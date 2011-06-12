'''
Created on 23.4.2010

@author: xaralis
'''
from metrocar.user_management.models import Deposit, Account, AccountActivity

from helpers import UserEnabledTestCase

class TestAccountActivity(UserEnabledTestCase):
    def test_0_save(self):
        old_account_balance = self.user.account.balance
        d = Deposit(account=self.user.account, money_amount=300, credited=False)
        d.save()
        a = Account.objects.get(user=self.user)
        self.assert_equals(a.balance, old_account_balance + d.money_amount)
        self.assert_equals('deposit', d.content_type.model)
        
        d2 = Deposit(account=self.user.account, money_amount=300, credited=True)
        d.save()
        a = Account.objects.get(user=self.user)
        self.assert_equals(a.balance, old_account_balance + d.money_amount)
        
    def test_1_as_concrete_class(self):
        d = Deposit(account=self.user.account, money_amount=300, credited=True)
        d.save()
        
        acc_act = AccountActivity.objects.get(pk=d.pk)
        self.assert_equals(acc_act.money_amount, 300)
        self.assert_true(isinstance(acc_act.as_concrete_class(), Deposit))
