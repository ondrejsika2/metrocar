'''
Created on 17.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.views import logout

urlpatterns = patterns('',
    # service urls
    url('%s/' % slugify(_('login')), 'mfe.users.views.login', name='mfe_users_login'),
    url('%s/' % slugify(_('logout')), logout, { 'next_page': '/' }, name='mfe_users_logout'),
    
    # registration
    url('%s/' % slugify(_('registration')), 'mfe.users.views.registration', name='mfe_users_registration'),
    
    # location search
    url(r'^search/$', 'mfe.utils.views.search', name='mfe_utils_search'),
)
