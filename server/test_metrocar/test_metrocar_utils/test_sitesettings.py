'''
Created on 23.4.2010

@author: xaralis
'''
import django.test

from metrocar.utils.models import SiteSettings

class TestSiteSettings(django.test.TestCase):
    def test_0_manager(self):
        current = SiteSettings.objects.get_current()
        self.assertEquals(isinstance(current, SiteSettings), True)
            
    def test_0_settings_dict(self):
        current = SiteSettings.objects.get_current()
        self.assertEquals(isinstance(current.get_unit_settings_dict(), dict), True)
