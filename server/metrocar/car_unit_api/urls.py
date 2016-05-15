from django.conf.urls.defaults import patterns, url

from metrocar.car_unit_api.views import StoreLog, Reservations, DataUploadView, JourneyAPI, ReservationCheckIn


urlpatterns = patterns('',
    url(r'^log/$', StoreLog.as_view(), name='store-log'),
    url(r'^reservations/$', Reservations.as_view(), name='reservations'),
    url(r'^journey/$', JourneyAPI.as_view(), name='journey'),
    url(r'^dataUpload/$', DataUploadView.as_view(), name='journey'),
    url(r'^reservationCheckIn/$', ReservationCheckIn.as_view(), name='reservation-check-in'),
)
