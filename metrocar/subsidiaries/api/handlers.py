'''
Created on 27.3.2010

@author: xaralis
'''

from piston.handler import BaseHandler

from metrocar.subsidiaries.models import * #@UnusedWildImport
    
class SubsidiaryHandler(BaseHandler):
    """
    Provides listing of subsidiaries.
    """
    allowed_methods = ('GET',)
    model = Subsidiary
    fields = ('name', 'url', 'email', 'street', 'house_number', 'city')
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_subsidiaries_subsidiary_handler', ['id'])
    
class SubsidiaryLocalHandler(BaseHandler):
    """
    Shows detailed information about current subsidiary (specified by 
    request HTTP domain).
    """
    allowed_methods = ('GET',)
    
    def read(self, request):
        """
        Returns information about current subsidiary (given by HTTP domain).
        """
        local = Subsidiary.objects.get_current()
        return local
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_subsidiaries_subsidiarylocal_handler', [])
    