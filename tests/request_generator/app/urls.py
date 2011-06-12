from django.conf.urls.defaults import *

from views import request_generator, http_proxy

urlpatterns = patterns('',
    url(r'^$', request_generator),
    url(r'^url/(?P<url>.*)$', http_proxy),
)