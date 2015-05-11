from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    (r'^api/', include('metrocar.car_unit_api.urls')),
    (r'^docs/', include('rest_framework_swagger.urls')),

    (r'^invoices/', include('metrocar.invoices.urls.backend')),

    (r'^tests/', include('metrocar.tests.urls')),

    (r'^', include(admin.site.urls)),

    url(r'^api/v1/', include('metrocar.urls_api')),

)


if settings.DEBUG:
    # serving static & media files in development
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
