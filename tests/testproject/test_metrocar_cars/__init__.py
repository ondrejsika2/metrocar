from datetime import date, datetime

from testproject.helpers import CarEnabledTestCase    

class CarTestCase(CarEnabledTestCase):
    def setUp(self):
        super(CarTestCase, self).setUp()