'''
Created on 10.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from django.conf import settings

from piston.resource import Resource

from metrocar.api.auth import get_authentication_handler

from handlers import *

auth = get_authentication_handler()

user_handler = Resource(UserHandler, authentication=auth)
account_handler = Resource(AccountHandler, authentication=auth)
reservation_handler = Resource(ReservationHandler, authentication=auth)
company_handler = Resource(CompanyHandler)

urlpatterns = patterns('',
    # companies
    url(r'^companies/$', company_handler, name='api_user_management_company_handler'),
    url(r'^companies/(?P<id>\d+)/$', user_handler, name='api_user_management_company_handler'),

    # users
    url(r'^$', user_handler, name='api_user_management_user_handler'),
    url(r'^(?P<username>[^/]+)/$', user_handler, name='api_user_management_user_handler'),
    url(r'^(?P<username>[^/]+)/account/$', account_handler, name='api_user_management_account_handler'),
    url(r'^(?P<username>[^/]+)/reservations/$', reservation_handler, name='api_user_management_reservations_handler'),
)