'''
Created on 10.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *

from piston.emitters import JSONEmitter, Emitter

from metrocar.utils.emitters import GeoJSONEmitter

# register custom emitters
JSONEmitter.unregister('json')
Emitter.register('json', GeoJSONEmitter, 'application/json; charset=utf-8')

urlpatterns = patterns('',
    url(r'api/cars/', include('metrocar.cars.api.urls')),
    url(r'api/users/', include('metrocar.user_management.api.urls')),
    url(r'api/subsidiaries/', include('metrocar.subsidiaries.api.urls')),
    url(r'api/pricelists/', include('metrocar.tarification.api.urls')),
    url(r'api/reservations/', include('metrocar.reservations.api.urls')),
    url(r'api/help/$', 'metrocar.api.views.documentation'),
    url(r'api/doc/$', 'metrocar.api.views.documentation'),
)