from djangosanetesting import UnitTestCase

from metrocar.cars.utils import grouping_precision


class TestGroupingPrecision(UnitTestCase):

    def test_default(self):
        location = 14.123456798, 50.123456789
        self.assert_equals(
            grouping_precision(location, default=4), (14.12346, 50.12346))
