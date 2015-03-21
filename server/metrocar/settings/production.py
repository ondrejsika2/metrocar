# Copy this to local.py and edit according to your needs.
from metrocar.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'metrocar',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_czech_ci',
    }
}

DEBUG = True
ALLOWED_HOSTS = [
    'localhost'
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
