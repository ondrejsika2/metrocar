# coding: utf-8
# Django settings for metrocar project.
from os.path import dirname, join
from tempfile import gettempdir

import metrocar, mfe

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERVE_STATIC_FILES = False

ADMINS = (
    ('Filip Varecha', 'xaralis@centrum.cz'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'metrocar_test'             # Or path to database file if using sqlite3.
DATABASE_USER = 'postgres'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

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
MEDIA_ROOT = dirname(metrocar.__file__) + '/../static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

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
    join( dirname( mfe.__file__ ), 'templates' ),
    join( dirname( metrocar.__file__ ), 'templates' ),
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

    #'django_evolution',
    'piston',
    'olwidget',
    'sorl.thumbnail',
    'django_tables',

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

    'mfe.active_pages',
    'mfe.cars',
    'mfe.reservations',
    'mfe.users',
    'mfe.utils',

    'testproject.test_metrocar_utils',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.request",
  "metrocar.subsidiaries.context_processors.subsidiary",
)

AUTHENTICATION_BACKENDS = ('metrocar.user_management.auth_backend.MetrocarBackend',)

ROOT_URLCONF = 'mfe.config.urls'

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
COMM_DTD_ROOT = MEDIA_ROOT + 'car_units/'
COMM_DTD_REQUEST = COMM_DTD_ROOT + 'request.dtd'
COMM_DTD_RESPONSE = COMM_DTD_ROOT + 'response.dtd'
COMM_GPX_SCHEMA = COMM_DTD_ROOT + 'gpx.xsd'

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
