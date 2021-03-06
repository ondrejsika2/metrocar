from django.conf.urls.defaults import patterns, url

from metrocar.car_unit_api.views import StoreLog, Reservations, DataUploadView, JourneyAPI, ReservationCheckIn, DefautPIDs, PingView


urlpatterns = patterns('',
    url(r'^log/$', StoreLog.as_view(), name='store-log'),
    url(r'^ping/$', PingView.as_view(), name='ping'),
    url(r'^reservations/$', Reservations.as_view(), name='reservations'),
    url(r'^journey/$', JourneyAPI.as_view(), name='journey'),
    url(r'^dataUpload/$', DataUploadView.as_view(), name='journey'),
    url(r'^reservationCheckIn/$', ReservationCheckIn.as_view(), name='reservation-check-in'),
    url(r'^downloadDefaultPids/$', DefautPIDs.as_view(), name='default-pids'),
)
