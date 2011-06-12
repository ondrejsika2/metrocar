import os, sys

''' cesta k pythonpath je nastavena pomoci apache'''
'''sys.path.insert(0, '/opt/iw/pythonpath')'''

os.environ['DJANGO_SETTINGS_MODULE'] = 'request_generator.settings_prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
