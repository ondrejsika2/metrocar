from mfe.settings import INSTALLED_APPS

INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'south']