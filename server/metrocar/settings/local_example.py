# Copy this to local.py and edit according to your needs.
from metrocar.settings.base import *
SECRET_KEY="skadjni,das.d,.3e2;3mkldasmdklas,.32"

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'metrocar',
        'HOST': 'localhost',
        'USER': 'metrocar',
        'PASSWORD': 'metrocar',
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_czech_ci',
    }
}

DEBUG = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# REST_FRAMEWORK = {
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.MultiPartParser',
#         'rest_framework.parsers.FileUploadParser',
#     )
# }


