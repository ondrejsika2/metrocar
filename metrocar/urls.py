from django.conf.urls.defaults import patterns, include
from django.conf import settings
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    (r'^api/', include('metrocar.car_unit_api.urls')),

    # Webservice API
    (r'^', include('metrocar.api.urls')),

    (r'^invoices/', include('metrocar.invoices.urls.backend')),

    (r'^', include(admin.site.urls)),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
