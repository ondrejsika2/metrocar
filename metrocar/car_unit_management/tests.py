import datetime

from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from metrocar.user_management.models import MetrocarUser
from metrocar.cars.models import Car
from metrocar.subsidiaries.models import Subsidiary
from metrocar.reservations.models import Reservation

class HandlerTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = MetrocarUser.objects.create_user(
            'pokus',
            'xaralis@centrum.cz',
            'voodoo',
            drivers_licence_number=111222,
            gender='M',
            identity_card_number=8761233,
            home_subsidiary=Subsidiary.objects.get_current()
        )
        
        self.reservation = Reservation.objects.create(
            user=self.user,
            car=Car.objects.get(pk=1),
            reserved_from=datetime.datetime(year=2010, month=2, day=25, hour=11, minute=55),
            reserved_until=datetime.datetime(year=2010, month=2, day=25, hour=19, minute=59),
        )
        self.reservation.save()
        
    @staticmethod
    def _get_request(filename):
        file = open(settings.CAR_UNIT_COMM_DTD_ROOT + filename)
        return file.read()
        
    def test_requests_without_reservation(self):
        request_filenames = ('request_1.xml', 'request_2.xml')
        
        for filename in request_filenames:
            request = self._get_request(filename)
            response = self.client.post('/comm/', request, content_type="text/xml")
            self.failUnlessEqual(response.status_code, 200)
            
    def test_request_reservation(self):
        request = self._get_request('request_3.xml')
        response = self.client.post('/comm/', request, content_type="text/xml")
        r2 = Reservation.objects.get(pk=self.reservation.pk)
        self.assertEquals(r2.started, datetime.datetime(2010, 2, 25, 12, 0))
        self.failUnlessEqual(response.status_code, 200)
        
        request = self._get_request('request_4.xml')
        response = self.client.post('/comm/', request, content_type="text/xml")
        r3 = Reservation.objects.get(pk=self.reservation.pk)
        self.assertEquals(r3.finished, 1)
        self.failUnlessEqual(response.status_code, 200)
        