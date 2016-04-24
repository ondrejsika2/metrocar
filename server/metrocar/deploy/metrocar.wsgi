import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'metrocar.settings.local'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
