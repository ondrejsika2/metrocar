'''
Created on 5.3.2010

@author: xaralis
'''

#from django.template.defaultfilters import slugify
#from django.utils.translation import gettext_lazy as _

from metrocar.settings import *


MFE_PATH = join(PROJECT_PATH, '..', 'mfe')


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

ROOT_URLCONF = 'mfe.urls'

TEMPLATE_DIRS += (
    join(MFE_PATH, 'templates'),
)

STATICFILES_DIRS += (
    join(MFE_PATH, 'static'),
)


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.messages.context_processors.messages',
    "metrocar.subsidiaries.context_processors.subsidiary",
)

LOGIN_URL = '/uzivatele/prihlaseni/'

SITE_ID = 1
