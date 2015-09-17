from metrocar.settings.base import *

if GEO_ENABLED:
    INSTALLED_APPS += INSTALLED_APPS_IF_GEO_ENABLED
else:
    GEOTRACK['BACKEND'] = 'geotrack.backends.dummy'    

if ACCOUNTING_ENABLED:
	INSTALLED_APPS += ('metrocar.accounting',)	
