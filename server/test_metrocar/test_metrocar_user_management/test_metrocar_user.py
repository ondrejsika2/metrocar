'''
Created on 23.4.2010

@author: xaralis
'''
import datetime
from nose.tools import raises

from metrocar.user_management.models import Account, UserCard, Deposit,\
    MetrocarUser, AccountActivity

from metrocar.invoices.models import Invoice

import django.test
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1


class TestMetrocarUser(django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        MetrocarUser.objects.all().delete()
        Account.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        MetrocarUser.objects.all().delete()

    def setUp(self):
        MetrocarUser.objects.all().delete()
        AccountActivity.objects.all().delete()
        Invoice.objects.all().delete()

        self.user_1 = create_user_1()

        self.acc_act1 = Deposit(account=self.user_1.account,
            money_amount=300, credited=False)
        self.acc_act1.save()


    def test_1_test_post_save_events(self):
        self.assertTrue(isinstance(self.user_1.account, Account))
        self.assertTrue(isinstance(self.user_1.user_card, UserCard))

    def test_2_get_invoice_address(self):
        pass # don't have business model to apply

    def test_3_get_uninvoiced(self):
        self.assertEquals(len(self.user_1.get_uninvoiced_account_activities()), 2)
        i = Invoice(user=self.user_1)
        i.save()
        self.assertEquals(len(MetrocarUser.objects.get(pk=self.user_1.pk).get_uninvoiced_account_activities()), 0)

    def test_4_get_invoiceable(self):
        self.assertEquals(len(self.user_1.get_invoiceable_activities()), 2)
        i = Invoice(user=self.user_1)
        i.save()
        self.assertEquals(len(MetrocarUser.objects.get(pk=self.user_1.pk).get_invoiceable_activities()), 0)

    def test_5_soft_delete(self):
        user_pk = self.user_1.pk
        self.user_1.delete()
        self.assertRaises(MetrocarUser.DoesNotExist, lambda: MetrocarUser.objects.get(pk=user_pk))
        self.assertTrue(MetrocarUser.objects.with_inactive().get(pk=user_pk))
