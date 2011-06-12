'''
Created on 23.4.2010

@author: xaralis
'''
from nose import SkipTest

from django.conf import settings

from djangosanetesting.cases import DatabaseTestCase

from metrocar.subsidiaries.models import Subsidiary
from django.core.urlresolvers import reverse

class TestContextProcessors(DatabaseTestCase):
    def setUp(self):
        if 'metrocar.subsidiaries.context_processors.subsidiary' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            raise SkipTest('Subsidiary context processor not enabled') 
    
    def test_0_test_ctxp_in_view(self):
        resp = self.client.get(reverse('mfe_cars_list')) # should be in urls..
        self.assert_equals(Subsidiary.objects.get_current().pk, resp.context['subsidiary'].pk)
        self.assert_equals(len(Subsidiary.objects.all()), len(resp.context['subsidiary_list']))