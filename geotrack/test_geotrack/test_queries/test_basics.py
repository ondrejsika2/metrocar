from django.test import TestCase

from geotrack.api import query
from geotrack.backends import get_backend
from geotrack.queries import load_universal_query
from testing_project.utils import entry


class TestQueryBasics(TestCase):

    def setUp(self):
        self.backend = get_backend()
        self.store = self.backend.store

    def test_query(self):
        self.store(**entry(unit_id=1, custom_field=-50))
        self.store(**entry(unit_id=1, custom_field=0))
        self.store(**entry(unit_id=1, custom_field=50))
        self.store(**entry(unit_id=1, custom_field=100))
        self.store(**entry(unit_id=2, custom_field=500))
        result = query('average', field='custom_field', units=[1])
        self.assertEqual(result, 25)

    def test_universal_query(self):
        self.store(**entry(unit_id=1, custom_field=-50))
        self.store(**entry(unit_id=1, custom_field=0))
        self.store(**entry(unit_id=1, custom_field=50))
        self.store(**entry(unit_id=1, custom_field=100))
        self.store(**entry(unit_id=2, custom_field=500))
        query = load_universal_query('average', self.backend)
        result = query(field='custom_field', units=[1])
        self.assertEqual(result, 25)
