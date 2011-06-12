'''
Created on 14.3.2010

@author: xaralis
'''

import urllib
import simplejson

from django.conf import settings
from django.utils.encoding import smart_str

class NominatimQuerier(object):
    forward_url = 'http://nominatim.openstreetmap.org/search?%s'
    reverse_url = 'http://nominatim.openstreetmap.org/reverse?%s'
    
    def make_query(self, url, params):
        """
        Urlencodes given param dict a performs a query to given url
        """
        f = urllib.urlopen(url % urllib.urlencode(params))
        return simplejson.load(f)
    
    def resolve_address(self, lat, lon):
        """
        Tries to resolve address for given lat and log and returns result 
        as dictionary.
        """
        params = {
            'format': 'json',
            'accept-language': settings.LANGUAGE_CODE,
            'lat': lat,
            'lon': lon,
            'zoom': 18,
            'addressdetails': 1,
            'email': settings.EMAIL_NOMINATIM
        }
        return self.make_query(self.reverse_url, params)
    
    def search_location(self, query):
        """
        Resolves query string in location and returns it as a dictionary
        """
        params = {
            'format': 'json',
            'accept-language': settings.LANGUAGE_CODE,
            'q': smart_str(query),
            'polygon': 0,
            'addressdedtails': 0,
            'email': settings.EMAIL_NOMINATIM
        }
        return self.make_query(self.forward_url, params)
        