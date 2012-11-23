# coding=utf-8
'''
Created on 23.4.2010

@author: xaralis
'''
from helpers import UserEnabledTestCase
from metrocar.user_management.forms import MetrocarUserCreationForm
from django.contrib.auth.models import User

class TestForms(UserEnabledTestCase):
    def setUp(self):
        super(TestForms, self).setUp()
        self.data = {
            'username': 'username',
            'password': 'somepass',
            'first_name': 'Roman',
            'last_name': u"Kubů",
            'email': 'roma.kubu@fel.cvut.cz',
            'primary_phone': '+420 123123123',
            'secondary_phone': '+420 123123123',
            'date_of_birth': '1900-01-01',
            'drivers_licence_number': '123123123',
            'identity_card_number': '123123123'
        }
        
    def test_0_creation_success_for_defaults(self):
        cf = MetrocarUserCreationForm(self.data)
        self.assert_false(cf.is_valid())
    
    def test_1_creation_fail_for_existing_username(self):
        self.data['username'] = self.user.username
        cf = MetrocarUserCreationForm(self.data)
        self.assert_false(cf.is_valid())
        
    def test_3_creation_fail_for_invalid_phone(self):
        self.data['primary_phone'] = '12313123'
        cf = MetrocarUserCreationForm(self.data)
        self.assert_false(cf.is_valid())
        
    def test_4_creation_fail_for_invalid_date(self):
        self.data['date_of_birth'] = '1.5.1986'
        cf = MetrocarUserCreationForm(self.data)
        self.assert_false(cf.is_valid())
        
    def test_duplicate_username(self):
        user = User.objects.create_user(username='username')
        data = {
            'username': 'username',
            'password': 'somepass',
            'first_name': 'Roman',
            'last_name': u"Kubů",
            'email': 'roma.kubu@fel.cvut.cz',
            'primary_phone': '420 123123123',
            'secondary_phone': '420 123123123',
            'date_of_birth': '1900-01-01',
            'language': 'CS',
            'drivers_licence_number': '123123123',
            'identity_card_number': '123123123'
        }
        form = MetrocarUserCreationForm(data)
        
        self.assert_false(form.is_valid())
