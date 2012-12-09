from djangosanetesting.cases import UnitTestCase

from metrocar.car_unit_api.validation import is_valid_location


class TestValidLocation(UnitTestCase):

    def test_valid(self):
        self.assertTrue(is_valid_location([10, -20.123]))

    def test_invalid(self):
        self.assertFalse(is_valid_location(['asdf', 123]))
