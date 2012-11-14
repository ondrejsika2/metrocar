from os.path import join, abspath, dirname

from mfe.settings import INSTALLED_APPS

INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'south']

FORCE_SELENIUM_TESTS = True

TEST_RUNNER = 'testrunner.DiscoveryDjangoTestSuiteRunner'
TEST_DISCOVERY_ROOT = BASE_PATH = abspath(join(dirname(__file__), '..'))
