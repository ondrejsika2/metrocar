from django.test import SimpleTestCase

from geotrack.queries.builtin.sparse_route import prune_to


class TestPruneTo(SimpleTestCase):

    def test_it(self):
        f = prune_to(5)
        self.assertEqual(f([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), [0, 2, 4, 6, 9])

    def test_empty(self):
        f = prune_to(10)
        self.assertEqual(f([]), [])

    def test_one_item(self):
        f = prune_to(5)
        self.assertEqual(f([42]), [42])
