# Django settings for testproject project.
from os.path import dirname, join

from metrocar.config.settings_base import *

import request_generator

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'metrocar'             # Or path to database file if using sqlite3.
DATABASE_USER = 'metrocar'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.

SERVE_STATIC_FILES = True
MEDIA_ROOT = '/var/www/python/metrocar.cz/static/'
STATIC_DOC_ROOT = '/var/www/python/metrocar.cz/static'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v8m01h*elj!#qgj702y@0s#=10+)anxmma6^iz-u7cxz0i&pf2'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join( dirname( request_generator.__file__ ), 'templates' ),
)

ROOT_URLCONF = 'request_generator.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'request_generator.app',
)

