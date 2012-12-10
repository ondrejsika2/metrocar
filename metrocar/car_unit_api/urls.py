from django.conf.urls.defaults import patterns, url

from metrocar.car_unit_api.views import StoreLog, Reservations


urlpatterns = patterns('',
    url(r'^log/$', StoreLog.as_view(), name='store-log'),
    url(r'^reservations/$', Reservations.as_view(), name='reservations'),
)
