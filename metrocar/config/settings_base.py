# coding=utf-8

# Django settings for metrocar project.
from os.path import dirname
from os.path import join

import metrocar

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERVE_STATIC_FILES = False

ADMINS = (
          ('Jan Wagner', 'wagnejan@fel.cvut.cz.cz')
          )

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Prague'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'cs'
LANG_CHOICES = (('CS', u'Česky'), ('EN', 'English'),)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = dirname(metrocar.__file__) + '../static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX =  '/metrocar/../static/admin/'



# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ry^a*eigc1p!d*j*gocmqsx3padg#(8g$nytui=+%#hjz@ck12'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
                    'django.template.loaders.filesystem.load_template_source',
                    'django.template.loaders.app_directories.load_template_source',
                    #     'django.template.loaders.eggs.load_template_source',
                    )

TEMPLATE_DIRS = (
                 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
                 # Always use forward slashes, even on Windows.
                 # Don't forget to use absolute paths, not relative paths.
                 join(dirname(metrocar.__file__), 'templates'),
                 )

MIDDLEWARE_CLASSES = (
                      'django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
                      )

INSTALLED_APPS = (
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.flatpages',
                  'grappelli',
                  'django.contrib.admin',
                  'django.contrib.admindocs',
                  'django.contrib.gis',
                  'django.contrib.markup',
                  'django_evolution',
                  'piston',
                  'olwidget',
                  'sorl.thumbnail',
                  'metrocar.car_unit_management', # needs to be first because it exports comm handler
                  'metrocar.api',
                  'metrocar.cars',
                  'metrocar.invoices',
                  'metrocar.reservations',
                  'metrocar.tariffs',
                  'metrocar.tarification',
                  'metrocar.user_management',
                  'metrocar.utils',
                  'metrocar.utils.flatpagesmeta',
                  'metrocar.subsidiaries',
                  )

TEMPLATE_CONTEXT_PROCESSORS = (
                               "django.core.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.request",
                               )

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'D, d.m.Y H:i'
CALENDAR_DATE_FORMAT = '%d.%m.%Y'
CALENDAR_TIME_FORMAT = '%H:%M'

#EMAIL SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'metrocar.mail@gmail.com'
EMAIL_HOST_PASSWORD = '4ut1ck40'
EMAIL_PORT = 587
EMAIL_USE_TLS = 1 #True

EMAIL_NOMINATIM = 'xaralis@centrum.cz'

COMM_TIME_FORMAT = '%y-%m-%d %H:%M'
COMM_OUTPUT_ENCODING = 'windows-1252'
COMM_INPUT_ENCODING = 'utf-8'
COMM_AUTHENTICATION_REQUIRED = False
COMM_DTD_ROOT = MEDIA_ROOT + 'car_units/'
COMM_DTD_REQUEST = '/home/komarem/metrocar/static/car_units/request.dtd'
COMM_DTD_RESPONSE ='/home/komarem/metrocar/static/car_units/response.dtd'
COMM_GPX_SCHEMA = COMM_DTD_ROOT + 'gpx.xsd'

# plugins to be used in reservation creation
RESERVATION_PLUGINS = (
                       'metrocar.reservations.plugins.AddReminderPlugin',
                       'metrocar.reservations.plugins.SendEmailPlugin',
                       )

# interval of cron service handling reminders
RESERVATION_REMINDER_CRON_INTERVAL = 60

# days to add from current date to generate DUE DATE
INVOICE_DUE_DATE_INTERVAL = 15

# if an invoice is overdue, multiply its amount by this constant and add
#to next month invoice as penalty
OVERDUE_INVOICE_PENALTY_RATE = 0.1 

SERIALIZATION_MODULES = {
    'python_deep': 'metrocar.utils.serializers.python'
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

ROOT_URLCONF = 'metrocar.config.urls'

SITE_ID = 1

DEFAULT_CHARSET = 'utf-8'
APPROXIMATE_DISTANCE_PER_HOUR = 10 # 10 km per hour
