#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils import unittest
from django.test.client import Client
from django.conf import settings

from metrocar.user_management.models import MetrocarUser
from metrocar.helpdesk.models import Ticket, Queue

from django.core.mail import send_mail
from django.core import mail

from fixtures import create_admin_only, create_ticket, create_queue, create_customer_only
from django.utils.translation import ugettext_lazy as _, ugettext

class TicketModelTestCase(unittest.TestCase):
    """
    Unit tests for Ticket class.
    """            
    def setUp(self):
        """
        Set up test classes and instances.
        """
        self.admin = create_admin_only()
        admin = MetrocarUser.objects.get(username=self.admin.username)
        self.assertEqual(admin.username, self.admin.username)
        
        self.q = create_queue() # create queue
        self.t = create_ticket(self.q) # create ticket

    def test_get_assigned_to_no_solver(self):
        """
        Ticket is unassigned, return value of method _get_assigned_to should match it.
         """
        self.t.assigned_to = None
        solver = self.t._get_assigned_to()
        self.assertEqual(solver,_('Unassigned'))
        
    def test_get_assigned_to_with_solver_with_full_name(self):
        """
        Ticket is assigned, admin has full name, return value of method _get_assigned_to should match admin's full name.
        """
        self.t.assigned_to = self.admin
        solver = self.t._get_assigned_to()
        self.assertEqual(solver,self.admin.get_full_name())        

    def test_get_assigned_to_with_solver_no_full_name(self):
        """
        Ticket is assigned, admin has NOT full name,
        return value of method _get_assigned_to should NOT match admin's full name,
        but it should match admin's username.
        """
        self.admin.first_name = ''
        self.admin.last_name = ''
        self.admin.save()        
        self.t.assigned_to = self.admin
        solver = self.t._get_assigned_to()
        self.assertNotEqual(solver,self.admin.get_full_name())  
        self.assertEqual(solver, self.admin.username)

class QueueModelTestCase(unittest.TestCase):
    """
    Unit tests for Queue class. This class has no testable methods.
    This test case simply tests the way that is used to verify if ticket is in some queue.
    """   
    def setUp(self):
        """
        Set up test classes and instances.
        """
        self.q1 = create_queue() # create queue
        self.q2 = create_queue() # create queue
        
        self.t1 = create_ticket(self.q1) # create ticket in q1
        self.t2 = create_ticket(self.q2) # create ticket in q2     

    def test_tickets_in_queues(self):
        """
        Simple test of queues and their related tickets.
        """
        self.assertTrue(self.t1 in self.q1.ticket_set.all())
        self.assertFalse(self.t1 in self.q2.ticket_set.all())
        self.assertTrue(self.t2 in self.q2.ticket_set.all())
        self.assertTrue(self.t2 not in self.q1.ticket_set.all())

from django.core.urlresolvers import reverse   
from django.test.client import RequestFactory   
from helpdesk.views.customer import index as CustomerIndexView 
from helpdesk.views.customer import ticket_supplement as CustomerSupplementTicketView 
from helpdesk.views.customer import show_ticket as CustomerShowTicketView 
from django.http import Http404
class CustomerViewsTestCase(unittest.TestCase):
    """
    Tests Customers views - index, supplement, etc.
    """
    def setUp(self):
        """
        Set up test classes and instances.
        """
        self.customer = create_customer_only()
        customer = MetrocarUser.objects.get(username=self.customer.username)
        self.assertEqual(customer.username, self.customer.username)  
        
        self.customer2 = create_customer_only()
        customer2 = MetrocarUser.objects.get(username=self.customer2.username)
        self.assertEqual(customer2.username, self.customer2.username)  
        
        self.factory = RequestFactory()
        
        self.q1 = create_queue() # create queue    
        self.t1 = create_ticket(self.q1) # create ticket in q1
        
        self.t1.who_reported = self.customer
        self.t1.who_created = self.customer
        self.t1.save()
        
        self.t2 = create_ticket(self.q1) # create ticket in q1
        
        self.t2.who_reported = self.customer
        self.t2.who_created = self.customer
        self.t2.status = Ticket.SUPPLEMENT_NEEDED_STATUS
        self.t2.save()
        
        self.t3 = create_ticket(self.q1) # create ticket in q1
        
        self.t3.who_reported = self.customer
        self.t3.who_created = self.customer
        self.t3.status = Ticket.SUPPLEMENT_NEEDED_STATUS
        self.t3.save()
        
   
    def test_customer_index_show_new_ticket(self):
        """
        Appearance of new ticket reported by customer on customer's index page.
        """
        request = self.factory.get(reverse('helpdesk_customer_index'))
        request.user = self.customer
        response = CustomerIndexView(request)
        self.assertEqual(response.status_code, 200) # successfull response
        self.assertTrue(self.t1.title in response.__str__()) # reported ticket is on index page
   
    #@unittest.expectedFailure # not used, the result is not as descriptive as explicit control of Http404 exception
    def test_customer_show_ticket_view(self):
        """
        Test show ticket view.
        1. Customer that reported this ticket will be able to access page with ticket overview.
        2. Customer that did not report this ticket won't be able to acces page with ticket overview,
        and an excepction will be risen.
        """        
        # customer that reported this ticket
        request = self.factory.get('/customer/show/' + str(self.t1.id))
        request.user = self.customer
        response = CustomerShowTicketView(request, self.t1.id)
        self.assertEqual(response.status_code, 200) # successfull response
        self.assertTrue(self.t1.title in response.__str__())
        self.assertTrue(self.t1.description in response.__str__())
        # customer that did not report this ticket
        request = self.factory.get('/customer/show/' + str(self.t1.id))
        request.user = self.customer2
        try:
            response = CustomerShowTicketView(request, self.t1.id)
        except Http404:
            self.assertTrue(True)
            return
        self.fail("Http404 not caught.")
        
    def test_customer_index_show_ticket_supplement_in_table(self):
        """
        Appearance of ticket with supplement needed status on customer's index page.
        """
        request = self.factory.get(reverse('helpdesk_customer_index'))
        request.user = self.customer
        response = CustomerIndexView(request)
        self.assertEqual(response.status_code, 200) # successfull response
        self.assertTrue(self.t2.title in response.__str__()) # reported ticket is on index page
        
        # anchor to ticket supplement should be on the page
        self.assertTrue('<td><a href=\"/bugrep/customer/supplement/' + str(self.t2.id) + '\">Doplnění</a></td>' in response.__str__())

        
    def test_customer_ticket_supplement(self):
        """    
        1. Access to customer's ticket supplement page.
        2. Fill in ticket supplement form and send it.
        3. Check updated ticket on web and in database.
        """
        # access
        request = self.factory.get('/bugrep/customer/supplement/' + str(self.t3.id))
        request.user = self.customer      
        response = CustomerSupplementTicketView(request, self.t3.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.t3.title in response.__str__())  
        # fill and send form
        request2 = self.factory.post('/bugrep/customer/supplement/' + str(self.t3.id))
        request2.POST['description'] = 'More accurate description'
        request2.user = self.customer
        response2 = CustomerSupplementTicketView(request2, self.t3.id)
        self.assertEqual(response2.status_code, 302) # should be redirected to customer's index
        self.assertEqual(response2['location'], '/bugrep/customer/')
        # check update
        request3 = self.factory.get(response2['location'])
        request3.user = self.customer
        response3 = CustomerIndexView(request)
        self.assertFalse('<td><a href="/bugrep/customer/supplement/' + str(self.t3.id) + '">Doplnění</a></td>' in response3.__str__())
        updated_t3 = Ticket.objects.get(pk=self.t3.id)
        self.assertTrue(updated_t3.status != self.t3.status)
        self.assertEqual(updated_t3.status, Ticket.NEW_STATUS)
			
from helpdesk.models import KBCategory, KBItem
from helpdesk.views.kb import item as KBItemView
from helpdesk.views.kb import vote as KBItemVote
class KnowledgeBaseTestCase(unittest.TestCase):
    """
    Unit tests for knowledge base.
    """   
    def setUp(self):
        """
        Set up test classes and instances.
        """
        KBCategory.objects.all().delete()
        self.kbcat1 = KBCategory(title='Nazev kategorie XAXAXA',slug='slug_XAXA',description='Popis kategorie XAXAXA')   
        self.kbcat1.save()
        
        self.kbitem1 = KBItem(category=self.kbcat1, title='Nazev clanku XAXAXA', question='Otazka XAXAXA', answer='Odpoved XAXAXA')
        self.kbitem1.save()
        
        self.kbitem2 = KBItem(category=self.kbcat1, title='Nazev clanku YAYAYA', question='Otazka YAYAYA', answer='Odpoved YAYAYA')
        self.kbitem2.save()
        
        self.client = Client()
        
        self.customer = create_customer_only()
        customer = MetrocarUser.objects.get(username=self.customer.username)
        self.assertEqual(customer.username, self.customer.username)  
        self.factory = RequestFactory()

    def test_kb_index(self):
        """
        Test appearance of knowledge base category on KB index page.
        """
        response = self.client.get(reverse('helpdesk_kb_index'))
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.kbcat1.title in response.__str__())
        self.assertTrue(self.kbcat1.description in response.__str__())     
        
    def test_kb_category_page(self):
        """
        Test appearance of KB item on KB category page. All should be present.
        """
        response = self.client.get('/bugrep/kb/' + self.kbcat1.slug, follow=True)
        self.assertEqual(200, response.status_code)
        # information about category
        self.assertTrue(self.kbcat1.title in response.__str__())
        self.assertTrue(self.kbcat1.description in response.__str__())
        # items in category
        self.assertTrue(self.kbitem1.title in response.__str__())
        self.assertTrue(self.kbitem1.question in response.__str__())

    def test_kb_item_view(self):
        """
        Test information shown about KB item. All should be present.
        """
        response = self.client.get('/bugrep/kb/' + str(self.kbitem1.id), follow=True)
        self.assertEqual(200, response.status_code)
        # information about item
        self.assertTrue(self.kbitem1.title in response.__str__())
        self.assertTrue(self.kbitem1.question in response.__str__())
        self.assertTrue(self.kbitem1.answer in response.__str__())
        
    def test_customer_kb_item_upvote(self):
        """
        Test customer's view (same for all logged-in users) of KB item and upvoting this item.
        Both item votes and recommendations should increase by one.
        """
        # create request to item view
        request = self.factory.get('/bugrep/kb/' + str(self.kbitem1.id))
        request.user = self.customer
        
        response = KBItemView(request, self.kbitem1.id)
        self.assertEqual(200, response.status_code)
        
        # check information shown about item
        self.assertTrue(self.kbitem1.title in response.__str__())
        self.assertTrue(self.kbitem1.question in response.__str__())
        self.assertTrue(self.kbitem1.answer in response.__str__())
        
        # check votes
        self.assertTrue(('<li>Doporučení: %s</li>' % self.kbitem1.recommendations) in response.__str__())
        self.assertTrue(('<li>Hlasy: %s</li>' % self.kbitem1.votes) in response.__str__())
        
        # upvote this item
        request2 = self.factory.get('/bugrep/kb/' + str(self.kbitem1.id) + '/vote/', {'vote':'up'})
        request2.user = self.customer
        response2 = KBItemVote(request2, self.kbitem1.id)
        self.assertEqual(302, response2.status_code)
        self.assertEqual(response2['location'],'/bugrep/kb/' + str(self.kbitem1.id) + '/')
        
        # check new votes
        request3 = self.factory.get(response2['location'])
        request3.user = self.customer
        response3 = KBItemView(request, self.kbitem1.id)
        self.assertEqual(200, response3.status_code)
        # check info in DB
        updated_item = KBItem.objects.get(pk=self.kbitem1.id)
        self.assertEquals(updated_item.votes, self.kbitem1.votes+1)
        self.assertEquals(updated_item.recommendations, self.kbitem1.recommendations+1)
        
        # check info in HTML
        self.assertFalse(('<li>Doporučení: %s</li>' % self.kbitem1.recommendations) in response3.__str__())
        self.assertFalse(('<li>Hlasy: %s</li>' % self.kbitem1.votes) in response3.__str__())        
        self.assertTrue(('<li>Doporučení: %s</li>' % updated_item.recommendations) in response3.__str__())
        self.assertTrue(('<li>Hlasy: %s</li>' % updated_item.votes) in response3.__str__())           
    
    def test_customer_kb_item_downvote(self):
        """
        Test customer's view (same for all logged-in users) of KB item and downvoting this item.
        Item recommendations should be the same, item votes should increase by one.
        """
        # create request to item view
        request = self.factory.get('/bugrep/kb/' + str(self.kbitem2.id))
        request.user = self.customer
        
        response = KBItemView(request, self.kbitem2.id)
        self.assertEqual(200, response.status_code)
        
        # check information shown about item
        self.assertTrue(self.kbitem2.title in response.__str__())
        self.assertTrue(self.kbitem2.question in response.__str__())
        self.assertTrue(self.kbitem2.answer in response.__str__())
        
        # check votes
        self.assertTrue(('<li>Doporučení: %s</li>' % self.kbitem2.recommendations) in response.__str__())
        self.assertTrue(('<li>Hlasy: %s</li>' % self.kbitem2.votes) in response.__str__())
        
        # downvote this item
        request2 = self.factory.get('/bugrep/kb/' + str(self.kbitem2.id) + '/vote/', {'vote':'down'})
        request2.user = self.customer
        response2 = KBItemVote(request2, self.kbitem2.id)
        self.assertEqual(302, response2.status_code)
        self.assertEqual(response2['location'],'/bugrep/kb/' + str(self.kbitem2.id) + '/')
        
        # check new votes
        request3 = self.factory.get(response2['location'])
        request3.user = self.customer
        response3 = KBItemView(request, self.kbitem2.id)
        self.assertEqual(200, response3.status_code)
        # check info from DB
        updated_item = KBItem.objects.get(pk=self.kbitem2.id)
        self.assertEquals(updated_item.votes, self.kbitem2.votes+1)
        self.assertEquals(updated_item.recommendations, self.kbitem2.recommendations)
        # check info in HTML
        self.assertTrue(('<li>Doporučení: %s</li>' % self.kbitem2.recommendations) in response3.__str__())
        self.assertFalse(('<li>Hlasy: %s</li>' % self.kbitem2.votes) in response3.__str__())        
        self.assertTrue(('<li>Doporučení: %s</li>' % updated_item.recommendations) in response3.__str__())
        self.assertTrue(('<li>Hlasy: %s</li>' % updated_item.votes) in response3.__str__())                              
        

if __name__ == '__main__':
    unittest.main()
