# Django settings for msekostala project.

from settings_base import *

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'metrocar'             # Or path to database file if using sqlite3.
DATABASE_USER = 'komarem'             # Not used with sqlite3.
DATABASE_PASSWORD = 'kleslo1234'         # Not used with sqlite3.

SERVE_STATIC_FILES = True
MEDIA_ROOT = '/home/komarem/metrocar/static/'
STATIC_DOC_ROOT = '/home/komarem/metrocar/static/'
STATIC_URL = '/static/'

