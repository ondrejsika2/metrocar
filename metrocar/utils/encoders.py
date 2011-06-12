'''
Created on 2.4.2010

@author: xaralis
'''

import simplejson

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.gis.geos.geometry import GEOSGeometry

class GeoJSONEncoder(DjangoJSONEncoder):
    """
    DateTimeAwareJSONEncoder subclass that knows how to serialize geometry to 
    GeoJSON format.
    """

    def default(self, o):
        if isinstance(o, GEOSGeometry):
            """
            This is very ugly. It first encodes the thing in GeoJSON and 
            then loads it as python structure.
            The purpose of this is that we need encodable structure for
            the JSON encoder, otherwise, it's all escaped and unreadable.
            """
            python_rep = simplejson.loads(o.geojson)
            return python_rep
        else:
            return super(GeoJSONEncoder, self).default(o) 

