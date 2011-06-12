'''
Created on 23.4.2010

@author: xaralis
'''
from nose.tools import raises

from metrocar.user_management.models import Account, UserCard, Deposit,\
    MetrocarUser, AccountActivity, UserRegistrationRequest

from helpers import UserEnabledTestCase
from metrocar.invoices.models import Invoice

class TestMetrocarUser(UserEnabledTestCase):
    def setUp(self):
        super(TestMetrocarUser, self).setUp()
        
        for a in AccountActivity.objects.filter(account__user=self.user):
            a.delete()
        
        self.acc_act1 = Deposit(account=self.user.account,
            money_amount=300, credited=False)
        self.acc_act1.save()
        self.acc_act2 = Deposit(account=self.user.account,
            money_amount=300, credited=True)
        self.acc_act2.save()
    
    def test_0_test_post_save_events(self):
        self.assert_true(isinstance(self.user.account, Account))
        self.assert_true(isinstance(self.user.user_card, UserCard))
        
    def test_1_get_absolute_url(self):
        self.assert_true(isinstance(self.user.get_absolute_url(), str))
        
    def test_2_get_invoice_address(self):
        pass # don't have business model to apply
    
    def test_3_get_uninvoiced(self):
        self.assert_equals(len(self.user.get_uninvoiced_account_activities()), 2)
        i = Invoice(user=self.user)
        i.save()
        self.assert_equals(len(MetrocarUser.objects.get(pk=self.user.pk).get_uninvoiced_account_activities()), 0)
    
    def test_4_get_invoiceable(self):
        self.assert_equals(len(self.user.get_invoiceable_activities()), 2)
        i = Invoice(user=self.user)
        i.save()
        self.assert_equals(len(MetrocarUser.objects.get(pk=self.user.pk).get_invoiceable_activities()), 0)
        
    def test_5_soft_delete(self):
        user_pk = self.user.pk
        self.user.delete()
        self.assert_raises(MetrocarUser.DoesNotExist, lambda: MetrocarUser.objects.get(pk=user_pk))
        self.assert_true(MetrocarUser.objects.with_inactive().get(pk=user_pk))
        
    def test_6_create_user(self):
        u = MetrocarUser.objects.create_user('u2', 'u2@test.cz', 'u2p')
        self.assert_raises(MetrocarUser.DoesNotExist, lambda: MetrocarUser.objects.get(pk=u.pk))
        self.assert_true(MetrocarUser.objects.with_inactive().get(pk=u.pk))
        self.assert_true(UserRegistrationRequest.objects.get(user=u))
            