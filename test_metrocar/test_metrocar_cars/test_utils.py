import django.test

from metrocar.cars.utils import grouping_precision


class TestGroupingPrecision(django.test.TestCase):

    def test_default(self):
        location = 14.123456798, 50.123456789
        self.assertEquals(
            grouping_precision(location, default=4), (14.12346, 50.12346))
