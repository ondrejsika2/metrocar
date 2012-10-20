from django.test import TestCase

from geotrack.backends import get_backend

from universal_backend_test import BackendTest


class TestGeodjango(BackendTest, TestCase):

    backend = get_backend('geotrack.backends.geodjango')
