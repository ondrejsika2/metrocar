# Django settings for metrocar project.
from os.path import dirname, join
from settings import *


DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'metrocar'             # Or path to database file if using sqlite3.
DATABASE_USER = 'metrocar'             # Not used with sqlite3.
DATABASE_PASSWORD = 'N6GPJ82KuTFM'         # Not used with sqlite3.


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_STATIC_FILES = False

# Absolute path to the directory that holds media.^
# Example: "/home/media/media.lawrence.com/"^
MEDIA_ROOT = '/var/www/metrocar/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a^
# trailing slash if there is a path component (optional in other cases).^
# Examples: "http://media.lawrence.com", "http://example.com/media/"^
MEDIA_URL = 'http://static.metrocar.dev.vlasta.fragaria.cz/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a^
# trailing slash.^
# Examples: "http://foo.com/media/", "/media/".^
ADMIN_MEDIA_PREFIX = 'http://static.metrocar.dev.vlasta.fragaria.cz/admin/'

