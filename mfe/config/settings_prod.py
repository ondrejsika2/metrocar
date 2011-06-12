'''
Created on 5.3.2010

@author: xaralis
'''

#from django.template.defaultfilters import slugify
#from django.utils.translation import gettext_lazy as _

from metrocar.config.settings_base import *

import mfe

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS += (
    'django.contrib.messages',    
    'django_tables',
    'mfe.active_pages',
    'mfe.cars',
    'mfe.reservations',
    'mfe.users',
	'mfe.utils',
)

# authentication backend for frontend use, uses MetrocarUser instead of 
# basic Django user
AUTHENTICATION_BACKENDS = ('metrocar.user_management.auth_backend.MetrocarBackend',)

ROOT_URLCONF = 'mfe.config.urls'

TEMPLATE_DIRS += (
    join( dirname( mfe.__file__ ), 'templates' ),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.messages.context_processors.messages',
    "metrocar.subsidiaries.context_processors.subsidiary",
)

LOGIN_URL = '/uzivatele/prihlaseni/'

SECRET_KEY = 'lka234][pjl951.,;dah123998(+-;adh281la;ds*/.,c1;'

SITE_ID = 1
