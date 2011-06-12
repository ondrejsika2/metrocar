from django.conf.urls.defaults import *
from django.conf import settings

from metrocar.config.admin import admin

urlpatterns = patterns('',
    # car unit management communication interface
    (r'^comm/', include('metrocar.car_unit_management.urls')),
    
    # Webservice API
    (r'^', include('metrocar.api.urls')),
    
    (r'^invoices/', include('metrocar.invoices.urls.backend')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^', include(admin.site.urls)),
    
    (r'^grappelli/', include('grappelli.urls'))
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    )
