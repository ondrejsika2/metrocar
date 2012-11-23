from os.path import join, abspath, dirname

from mfe.settings import INSTALLED_APPS

INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'south']

TEST_RUNNER = 'testrunner.DiscoveryDjangoTestSuiteRunner'
TEST_DISCOVERY_ROOT = BASE_PATH = abspath(join(dirname(__file__), '..'))

LOCALE_PATHS = [
    join(BASE_PATH, '..', 'mfe', 'locale'),
]
