'''
Created on 27.3.2010

@author: xaralis
'''

from piston.handler import BaseHandler
from piston.utils import rc

from metrocar.tarification.models import *

class PricelistHandler(BaseHandler):
    """
    Stands as data source for pricelist information.
    
    Provides listings or detailed information about specific pricelist.
    """
    
    allowed_methods = ('GET',)
    model = Pricelist
    non_list_fields = ('name', ('model', ('resource_uri')))
    list_fields = non_list_fields + ('get_pricing_summary',)
    fields = non_list_fields
    
    def read(self, request, id=None):
        """
        Returns information about pricelists (pricelist name, car 
        model along with it's resource uri) or detailed information about 
        pricelist of given id (same as list but pricing summary is included).
        """
        if id is not None:
            try:
                self.fields = self.list_fields
                p = Pricelist.objects.valid().get(pk=id)
                return p
            except Pricelist.DoesNotExist:
                return rc.NOT_FOUND
        self.fields = self.non_list_fields
        return Pricelist.objects.valid()
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_pricelist_handler', ['id'])
    