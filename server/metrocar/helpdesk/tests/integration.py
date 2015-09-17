#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import unittest
from django.test.client import Client
from django.conf import settings
from fixtures import create_car, create_customer_only, create_reservation, create_technician_only, create_admin_only, create_queue
from django.core.urlresolvers import reverse  
from metrocar.user_management.models import MetrocarUser

from helpdesk.views.customer import report_defect as CustomerReportView
  
from django.test.client import RequestFactory   

from helpdesk.views.staff import create_ticket as CreateTicketView
from helpdesk.views.customer import index as CustomerIndexView 
from django.core import mail
from helpdesk.models import Ticket

class TicketFormCarSelectTestCase(unittest.TestCase):
    """
    This test tests right select options in defect report forms. Tests for Customer and Technician.
    """
    def setUp(self):
        # create test data
        self.car = create_car()
        self.not_reserved_car = create_car()
        
        self.customer = create_customer_only()
        customer = MetrocarUser.objects.get(username=self.customer.username)
        self.assertEqual(customer.username, self.customer.username)  
        
        self.technician = create_technician_only()
        technician = MetrocarUser.objects.get(username=self.technician.username)
        self.assertEqual(technician.username, self.technician.username)          
        
        self.admin = create_admin_only()
        admin = MetrocarUser.objects.get(username=self.admin.username)
        self.assertEqual(admin.username, self.admin.username)         

        self.reservation = create_reservation(p_user = self.customer, p_car = self.car)
        self.reservation = create_reservation(p_user = self.technician, p_car = self.car)
        self.reservation = create_reservation(p_user = self.admin, p_car = self.car)

        self.factory = RequestFactory()

    def test_customer_reserved_car_options_in_form_select(self):
        """
        Customer should see only cars that he reserved.
        """
        # create request for page with form
        request = self.factory.get(reverse('helpdesk_customer_report_defect'))
        request.user = self.customer
        # send request        
        response = CustomerReportView(request)
        # check status code and returned page content        
        self.assertEqual(response.status_code, 200) # successfull response
        self.assertTrue(self.car.__str__() in response.__str__()) # this car should be on the page
        self.assertFalse(self.not_reserved_car.__str__() in response.__str__()) # this car should not be on the page

    def test_technician_all_car_options_in_form_select(self):
        """ 
        Technician should see all cars in report form.
        """
        request = self.factory.get(reverse('helpdesk_submit'))
        request.user = self.technician
        
        response = CreateTicketView(request)
        
        self.assertEqual(response.status_code, 200) # successfull response
        self.assertTrue(self.car.__str__() in response.__str__()) # this car should be on the page
        self.assertTrue(self.not_reserved_car.__str__() in response.__str__()) # this car should also be on the page  

class TicketFormCarSelectTestCase(unittest.TestCase):
    """
    Tests customer report form.
    """
    def setUp(self):
        # create test data
        self.car = create_car()
        
        self.customer = create_customer_only()
        customer = MetrocarUser.objects.get(username=self.customer.username)
        self.assertEqual(customer.username, self.customer.username)  
        
        self.reservation = create_reservation(p_user = self.customer, p_car = self.car)

        self.factory = RequestFactory()
        
        self.q1 = create_queue()

    def test_customer_reserved_car_options_in_form_select(self):
        """
        Customer should be able to create new ticket with this form.
        """
        # create test ticket
        ticket_title = 'Shrnuti zavady XAXAXA'
        ticket_description = 'Detailni popis zavady'
        request = self.factory.post(reverse('helpdesk_customer_report_defect'))
        request.user = self.customer
        # set up POST data
        request.POST['queue'] = self.q1.id
        request.POST['title'] = ticket_title
        request.POST['body'] = ticket_description
        request.POST['which_car'] = self.car.id
        # send request        
        response = CustomerReportView(request)
        # check status code and response redirect        
        self.assertEqual(response.status_code, 302) # redirect to /bugrep/customer/
        self.assertEqual(response['location'],'/bugrep/customer/')
        # process redirection to overview of all ticket reported by this user      
        request2 = self.factory.get(response['location'])
        request2.user = self.customer
        response2 = CustomerIndexView(request2)
        
        self.assertEqual(response2.status_code, 200) # successfull get
        
        self.assertTrue(ticket_title in response2.__str__()) # this ticket should be on the page
        self.assertEqual(Ticket.objects.filter(title__exact=ticket_title).count(),1)

    def test_customer_title_too_long(self):
        """
        Length of titket title is limited, it should not be possible to send report with too long title (longer then 100 characters).
        """
        # create test ticket
        import random, string
        ticket_title = ''.join(random.choice(string.lowercase) for i in range(103))
        ticket_description = 'Detailni popis zavady'
        request = self.factory.post(reverse('helpdesk_customer_report_defect'))
        request.user = self.customer
        # set up POST data
        request.POST['queue'] = self.q1.id
        request.POST['title'] = ticket_title
        request.POST['body'] = ticket_description
        request.POST['which_car'] = self.car.id
        # send request        
        response = CustomerReportView(request)
        # title is too long, a warning message should appear on page
        # unfortunately, unicode characters (czech text) is problematic, so just a part of the message is tested (but it's unique)
        self.assertTrue('<span class="help-block ">Hodnota sm' in response.__str__())

from HTMLParser import HTMLParser
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            for name, value in attrs:
                if name == 'name':
                    if value == 'csrfmiddlewaretoken':
						for name, value in attrs:
							if name == 'value':
								self.csrf = value # save value of csrf token

                                 
class AuthenticationTestCase(unittest.TestCase):
    """
    This TestCase was created just to ensure that "standard" authentication ways do not work.
    """
    def setUp(self):
        """
        Set up test classes and instances.
        """
        self.customer = create_customer_only()
        customer = MetrocarUser.objects.get(username=self.customer.username)
        self.assertEqual(customer.username, self.customer.username)
        self.client = Client()    
        
    def test_simple_post(self):
        """
        Try to log in by sending simple POST request to login page.
        """
        response = self.client.get('/bugrep/login/')
        self.assertEquals(response.status_code,200)
        response = self.client.post('/bugrep/login/', {'username': self.customer.username, 'password': self.customer.password})
        self.assertTrue('Login' in response.__str__()) # unsuccessfull login - bad username and password, still on Login page          

    def test_post(self):
        """
        Try to log in by sending POST request to login page.
        It sends all data needed (along with csrf token and next parameters).
        This should normally work, successfully tested with Easy REST plugin to Mozilla Firefox (even without more headers).
        """
        response = self.client.get('/bugrep/login/')
        self.assertEquals(response.status_code,200)
        parser = MyHTMLParser()
        a = response.__str__()
        parser.feed(a)
        response = self.client.post('/bugrep/login/', {'username': self.customer.username, 'password': self.customer.password,
        'csrfmiddlewaretoken':parser.csrf, 'next':'../'}, content_type='application/x-www-form-urlencoded')
        self.assertTrue('Login' in response.__str__()) # unsuccessfull login - bad username and password, still on Login page

    def test_login(self):
        """
        Try to log in by using framework method, not working either. (login() should return True if successfully logged in)
        """
        self.assertFalse(self.client.login(username=self.customer.username, password=self.customer.password))
        
