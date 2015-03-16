'''
Created on 23.4.2010

@author: xaralis
'''
from helpers import UserEnabledTestCase
from metrocar.user_management.auth_backend import MetrocarBackend

class TestAuthBackend(UserEnabledTestCase):
    def setUp(self):
        super(TestAuthBackend, self).setUp()
        self.auth_bck = MetrocarBackend()
    
    def test_0_authenticate_success(self):
        self.assertTrue(self.auth_bck.authenticate(self.user.username, 'testpass'))
        
    def test_1_authenticated_bad_pass(self):
        self.assertFalse(self.auth_bck.authenticate(self.user.username, 'badpass'))
        
    def test_2_authenticated_bad_username(self):
        self.assertFalse(self.auth_bck.authenticate('badusername', 'testpass'))