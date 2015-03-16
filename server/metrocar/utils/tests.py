__author__="Xaralis"
__date__ ="$28.10.2009 17:26:34$"

    
from django.test import TestCase
from django.conf import settings

from metrocar.utils.models import SiteSettings

class SiteTest(TestCase):
    def test_manager(self):
        current = SiteSettings.objects.get_current()
        self.assertEquals(isinstance(current, SiteSettings), True)
            
    def test_settings_dict(self):
        current = SiteSettings.objects.get_current()
        self.assertEquals(isinstance(current.get_unit_settings_dict(), dict), True)
            
