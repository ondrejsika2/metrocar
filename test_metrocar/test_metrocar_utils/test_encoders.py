'''
Created on 23.4.2010

@author: xaralis
'''
from django.contrib.gis.geos.point import Point
from django.core.serializers.json import DjangoJSONEncoder

import django.test

from metrocar.utils.encoders import GeoJSONEncoder

class TestEncoders(django.test.TestCase):
    def setUp(self):
        self.encoder = GeoJSONEncoder()
    
    def test_0_encode_geometry(self):
        g = Point(10.5, 10.5)
        self.assertEquals(self.encoder.encode(g), '{"type": "Point", "coordinates": [10.5, 10.5]}')
        
    def test_0_encode_default(self):
        djangoencoder = DjangoJSONEncoder()
        self.assertEquals(self.encoder.encode('str'), djangoencoder.encode('str'))