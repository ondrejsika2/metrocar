# coding=utf-8

# Django settings for metrocar project.
from os.path import abspath, dirname, join


PROJECT_PATH = abspath(join(dirname(__file__), '..'))


DEBUG = True
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


# Static files ################################################################

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(PROJECT_PATH, '..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# User-uploaded files #########################################################

MEDIA_ROOT = join(PROJECT_PATH, '..', 'files')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/files/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ry^a*eigc1p!d*j*gocmqsx3padg#(8g$nytui=+%#hjz@ck12'


# Templates ##################################################################

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(PROJECT_PATH, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)


MIDDLEWARE_CLASSES = (
                      'django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
                      )

INSTALLED_APPS = (
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.flatpages',
                  'django.contrib.admin',
                  'django.contrib.admindocs',
                  'django.contrib.messages',
                  'django.contrib.gis',
                  'django.contrib.markup',
                  'django.contrib.staticfiles',

                  # TODO: use South instead
                  #'django_evolution',

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
COMM_DTD_ROOT = join(PROJECT_PATH, 'static', 'car_units')
COMM_DTD_REQUEST = join(COMM_DTD_ROOT, 'request.dtd')
COMM_DTD_RESPONSE = join(COMM_DTD_ROOT, 'response.dtd')
COMM_GPX_SCHEMA = join(COMM_DTD_ROOT, 'gpx.xsd')

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

# version string
VERSION = "1"

ROOT_URLCONF = 'metrocar.urls'

SITE_ID = 1

DEFAULT_CHARSET = 'utf-8'
DEFAULT_RESERVATION_DISTANCE = 10 # 10 km


# minimalni minutovy interval mezi zacatkem a koncem rezervace automobilu
RESERVATION_TIME_INTERVAL   = 30
# rezervaci je mozne si nacasovat po ctvrt hodine
RESERVATION_TIME_SHIFT      = 15
