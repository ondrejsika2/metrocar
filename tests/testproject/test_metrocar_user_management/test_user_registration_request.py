'''
Created on 23.4.2010

@author: xaralis
'''
from nose.tools import raises

from metrocar.user_management.models import UserRegistrationRequest,\
    MetrocarUser

from helpers import UserEnabledTestCase
from _mysql_exceptions import IntegrityError

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
        self.assert_equals(req.approved, False)
        self.assert_equals(req.resolved, False)
        
        req.approve()
        
        self.assert_equals(req.approved, True)
        self.assert_equals(req.resolved, True)
        
        u = MetrocarUser.objects.get(pk=self.user.pk)
        self.assert_equals(u.is_active, True)
        req.delete()
    
    def test_1_reject(self):
        self.user.is_active = False
        self.user.save()
        
        req = UserRegistrationRequest.objects.create_for_user(self.user)
        self.assert_equals(req.approved, False)
        self.assert_equals(req.resolved, False)
        
        req.reject()
        
        self.assert_equals(req.approved, False)
        self.assert_equals(req.resolved, True)
        
        u = MetrocarUser.objects.with_inactive().get(pk=self.user.pk)
        self.assert_equals(u.is_active, False)
        req.delete()
    
    @raises(IntegrityError)
    def test_3_unique(self):
        try:
            # reason why we are doing the test this way is because different
            # db backends have different IntegrityErrors so the error might
            # not been catched
            req = UserRegistrationRequest.objects.create_for_user(self.user)
            req2 = UserRegistrationRequest.objects.create_for_user(self.user)
        except:
            raise IntegrityError
        