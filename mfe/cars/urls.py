from django.conf.urls.defaults import patterns, url
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from mfe.cars import views


urlpatterns = patterns('',
    # car detail
    url(r'^%s/$' % slugify(_('car')), 'mfe.cars.views.car_detail', name='mfe_cars_detail'),
    url(r'^%s/(?P<id>\d+)/$' % slugify(_('car')), 'mfe.cars.views.car_detail', name='mfe_cars_detail'),

    url(r'^$', views.CarMap.as_view(), name='mfe_cars'),
    url(r'^map-data/$', views.CarMapData.as_view(), name='mfe_cars_map_data'),

    # car list
    # url(r'^$', 'mfe.cars.views.car_list', name='mfe_cars'),
    url(r'^%s/$' % slugify(_('find cars')), 'mfe.cars.views.car_list', name='mfe_cars_list'),
    url(r'^load_car_list/(?P<start_date>([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})+)/(?P<start_time>([0-9]{2}:[0-9]{2})+)/(?P<end_date>([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})+)/(?P<end_time>([0-9]{2}:[0-9]{2})+)/$', 'mfe.cars.views.load_car_list', name='mfe_load_car_list'),

    # parkings
    url(r'^%s/$' % slugify(_('parking list')), 'mfe.cars.views.parking_list', name='mfe_cars_parking_list'),

    # pricing
    url(r'^%s/$' % slugify(_('fares')), 'mfe.cars.views.fares', name='mfe_cars_fares'),

    # geo feeds
    # we have to provide url without parameter to allow using named urls
    # in js code
    url(r'^geo-feed/$', 'mfe.cars.views.geo_feed', name='mfe_cars_geo_feed'),
    url(r'^geo-feed/(?P<type>[a-z_-]+)/$', 'mfe.cars.views.geo_feed', name='mfe_cars_geo_feed_type'),

    # geo details feed
    # default url same as above
    url(r'^geo-details/$', 'mfe.cars.views.geo_details', name='mfe_cars_geo_detail'),
    url(r'^geo-details/(?P<type>[a-z_-]+)/(?P<id>\d+)/$', 'mfe.cars.views.geo_details', name='mfe_cars_geo_detail_type_id'),
)
