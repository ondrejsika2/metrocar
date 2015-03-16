import django.test

from metrocar.utils.geo.validation import is_valid_location, is_valid_polygon


class TestValidLocation(django.test.TestCase):

    def test_valid(self):
        self.assertTrue(is_valid_location([10, -20.123]))

    def test_invalid(self):
        self.assertFalse(is_valid_location(['asdf', 123]))


class TestValidPolygon(django.test.TestCase):

    def test_valid(self):
        self.assertTrue(is_valid_polygon([
            (10, -20.123),
            (11, 13),
            (5, 24.0),
            (10, -20.123),
        ]))

    def test_invalid_type(self):
        self.assertFalse(is_valid_polygon('assdf'))

    def test_invalid_location(self):
        self.assertFalse(is_valid_polygon([
            (10, -20.123, 234),
            (11, 13),
            (5, 24.0),
            (10, -20.123),
        ]))

    def test_not_enough_locations(self):
        self.assertFalse(is_valid_polygon([
            (10, -20.123),
            (11, 13),
        ]))
