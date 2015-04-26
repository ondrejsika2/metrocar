#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import unittest
from django.test.client import Client
from django.conf import settings

from metrocar.user_management.models import MetrocarUser
from fixtures import create_admin_only

from django.core.mail import send_mail
from django.core import mail

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = create_admin_only()
        admin = MetrocarUser.objects.get(username=self.admin.username)
        self.assertEqual(admin.username, self.admin.username)

    def testLoginPageAccesible(self):
        """
        Is Login page accessible?
        """
        response = self.client.get('/bugrep/login/')
        self.assertEqual(response.status_code,200)
        
    def testMailService(self):
        """
        Is email service working?
        """
        send_mail('Subject here', 'Here is the message.', 'from@example.com',['to@example.com'], fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')

if __name__ == '__main__':
    unittest.main()
