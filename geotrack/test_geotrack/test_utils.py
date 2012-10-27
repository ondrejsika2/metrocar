from datetime import datetime

from django.test import SimpleTestCase

from geotrack.utils import extract_timestamp


class TestValidTimestamp(SimpleTestCase):

    def test_iso8601(self):
        self.assertEqual(extract_timestamp("2012-10-27T15:07:04.703Z"),
            datetime(2012, 10, 27, 15, 7, 4, 703000))
