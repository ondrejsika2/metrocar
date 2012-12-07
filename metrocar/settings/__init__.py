from metrocar.settings.base import *

try:
    from metrocar.settings.local import *
except ImportError:
    pass

if GEO_ENABLED:
    INSTALLED_APPS += INSTALLED_APPS_IF_GEO_ENABLED

else:
    GEOTRACK['BACKEND'] = 'geotrack.backends.dummy'
