'''
Created on 23.4.2010

@author: xaralis
'''
from nose.tools import raises

from metrocar.user_management.models import UserRegistrationRequest,\
    MetrocarUser

from helpers import UserEnabledTestCase


class TestUserRegistrationRequest(UserEnabledTestCase):
    def setUp(self):
        super(TestUserRegistrationRequest, self).setUp()

        requests = UserRegistrationRequest.objects.with_resolved().filter(user=self.user)
        for r in requests:
            r.delete()

    def test_0_approve(self):
        self.user.is_active = False
        self.user.save()

        req = UserRegistrationRequest.objects.create_for_user(self.user)
        self.assertEquals(req.approved, False)
        self.assertEquals(req.resolved, False)

        req.approve()

        self.assertEquals(req.approved, True)
        self.assertEquals(req.resolved, True)

        u = MetrocarUser.objects.get(pk=self.user.pk)
        self.assertEquals(u.is_active, True)
        req.delete()

    def test_1_reject(self):
        self.user.is_active = False
        self.user.save()

        req = UserRegistrationRequest.objects.create_for_user(self.user)
        self.assertEquals(req.approved, False)
        self.assertEquals(req.resolved, False)

        req.reject()

        self.assertEquals(req.approved, False)
        self.assertEquals(req.resolved, True)

        u = MetrocarUser.objects.with_inactive().get(pk=self.user.pk)
        self.assertEquals(u.is_active, False)
        req.delete()

    def test_3_unique(self):
        UserRegistrationRequest.objects.create_for_user(self.user)
        with self.assertRaises(Exception):
            UserRegistrationRequest.objects.create_for_user(self.user)
