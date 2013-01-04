from django.test import TestCase

from geotrack.backends import get_backend
from geotrack.test import BackendTest


class TestGeodjango(BackendTest, TestCase):

    backend = get_backend('geotrack.backends.geodjango')
