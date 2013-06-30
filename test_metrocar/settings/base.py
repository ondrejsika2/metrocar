# coding: utf-8
from metrocar.settings import *

from os.path import dirname, join
from tempfile import gettempdir

import metrocar
import mfe


DEBUG = False

TEMPLATE_DEBUG = DEBUG

SERVE_STATIC_FILES = False

ADMINS = (
    ('Filip Varecha', 'xaralis@centrum.cz'),
)

MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ry^a*eigc1p!d*j*gocmqsx3padg#(8g$nytui=+%#hjz@ck12'


if not GEO_ENABLED:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }


#deactivate accounting for tests
ACCOUNTING_ENABLED = False    

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join( dirname( mfe.__file__ ), 'templates' ),
    join( dirname( metrocar.__file__ ), 'templates' ),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

INSTALLED_APPS = [x for x in INSTALLED_APPS if x != 'south'] + [
    'test_metrocar.test_metrocar_utils',
]

TEMPLATE_CONTEXT_PROCESSORS += (
  "metrocar.subsidiaries.context_processors.subsidiary",
)

AUTHENTICATION_BACKENDS = ('metrocar.user_management.auth_backend.MetrocarBackend',)

ROOT_URLCONF = 'mfe.urls'

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'D, d.m.Y H:i'
CALENDAR_DATE_FORMAT = '%d.%m.%Y'
CALENDAR_TIME_FORMAT = '%H:%M'

EMAIL_ROBOT_FROM_ADDR = 'robot@metrocar.cz'
EMAIL_NOMINATIM = 'xaralis@centrum.cz'

COMM_TIME_FORMAT = '%y-%m-%d %H:%M'
COMM_OUTPUT_ENCODING = 'windows-1252'
COMM_INPUT_ENCODING = 'utf-8'
COMM_AUTHENTICATION_REQUIRED = False


# plugins to be used in reservation creation
RESERVATION_PLUGINS = (
    'metrocar.reservations.plugins.AddReminderPlugin',
    #'metrocar.reservations.plugins.SendEmailPlugin',
)

# interval of cron service handling reminders
RESERVATION_REMINDER_CRON_INTERVAL = 60

# days to add from current date to generate DUE DATE
INVOICE_DUE_DATE_INTERVAL = 15

SERIALIZATION_MODULES = {
    'python_deep' : 'metrocar.utils.serializers.python'
}

AUTH_PROFILE_MODULE = 'user_management.MetrocarUser'

# api authentication realm
API_AUTH_REALM = 'metrocar-backend'

# log path
LOG_PATH = 'log/metrocar.log'

# disable caching
CACHE_BACKEND = 'dummy:///'

# version string
VERSION = "1"

SITE_ID = 1

TEST_RUNNER = 'djangosanetesting.testrunner.DstNoseTestSuiteRunner'
