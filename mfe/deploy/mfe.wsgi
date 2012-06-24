import os, sys

''' cesta k pythonpath je nastavena pomoci apache'''
'''sys.path.insert(0, '/opt/iw/pythonpath')'''
sys.path.append('/home/komarem/metrocar/mfe/')
sys.path.append('/home/komarem/metrocar/pythonpath/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mfe.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
