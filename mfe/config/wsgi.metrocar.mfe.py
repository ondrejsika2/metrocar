import os, sys

''' cesta k pythonpath je nastavena pomoci apache'''
'''sys.path.insert(0, '/opt/iw/pythonpath')'''

os.environ['DJANGO_SETTINGS_MODULE'] = 'mfe.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
