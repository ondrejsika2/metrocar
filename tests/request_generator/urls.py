from django.conf.urls.defaults import *
from django.conf import settings

from metrocar.config.admin import admin

urlpatterns = patterns('',
    (r'^', include('request_generator.app.urls')),
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    )
