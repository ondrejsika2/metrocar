from datetime import datetime, timedelta

import django.test
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from metrocar.reservations.models import Reservation
from metrocar.user_management.models import MetrocarUser, Account
from test_metrocar.test_metrocar_cars.fixtures import create_car_1, create_pricelist_1
from test_metrocar.test_metrocar_reservation.fixtures import create_reservation_1
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1, create_user_admin_1


class TestReservationsApi(django.test.TestCase):

    @classmethod
    def setUpClass(cls):
        Reservation.objects.all().delete()
        MetrocarUser.objects.all().delete()
        Account.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Reservation.objects.all().delete()
        MetrocarUser.objects.all().delete()
        Account.objects.all().delete()

    def setUp(self):
        self.reservation_1 = create_reservation_1()

    def tearDown(self):
        Account.objects.all().delete()

    def test_perm_1(self):
        client = APIClient()
        response = client.get(reverse('reservation-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_perm_2(self):
        client = APIClient()
        client.force_authenticate(create_user_admin_1())
        response = client.get(reverse('reservation-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_list(self):
        client = APIClient()
        client.force_authenticate(self.reservation_1.user)
        response = client.get(reverse('reservation-list'))

        print response.data["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_detail_success(self):
        client = APIClient()
        client.force_authenticate(user=self.reservation_1.user)

        response = client.get(
            reverse('reservation-detail', kwargs={"pk": self.reservation_1.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_not_exist(self):
        client = APIClient()
        client.force_authenticate(user=create_user_1())

        response = client.get(
            reverse('reservation-detail', kwargs={"pk": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_not_permitted(self):
        client = APIClient()
        client.force_authenticate(user=create_user_admin_1())

        response = client.patch(
            reverse('reservation-detail', kwargs={"pk": self.reservation_1.id}),
            data={
                "reserved_from": datetime.now(),
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_success(self):
        client = APIClient()
        client.force_authenticate(user=self.reservation_1.user)

        response = client.patch(
            reverse('reservation-detail', kwargs={"pk": self.reservation_1.id}),
            data={
                "reserved_from": datetime.now(),
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_not_exist(self):
        client = APIClient()
        client.force_authenticate(user=self.reservation_1.user)

        response = client.patch(
            reverse('reservation-detail', kwargs={"pk": 9999}),
            data={
                "reserved_from": datetime.now(),
            })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        client = APIClient()
        client.force_authenticate(user=self.reservation_1.user)

        response = client.delete(
            reverse('reservation-detail', kwargs={"pk": self.reservation_1.id}))

        # deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(
            reverse('reservation-detail', kwargs={"pk": self.reservation_1.id}))

        # make sure if it is deleted
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_no_content(self):
        user_1 = create_user_1()

        client = APIClient()
        client.force_authenticate(user=user_1)

        response = client.post(reverse('reservation-list'), data={})

        # not all required data provided
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_success(self):
        user_1 = create_user_1()
        car_1 = create_car_1()
        create_pricelist_1(car_model=car_1.model)

        client = APIClient()
        client.force_authenticate(user=user_1)

        response = client.post(reverse('reservation-list'), data={
            "reserved_from": (datetime.now() + timedelta(hours=1)),
            "reserved_until": (datetime.now() + timedelta(hours=12)),
            "user": user_1.id,
            "car": car_1.id
        })

        # created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            reverse('reservation-detail', kwargs={"pk": response.data['id']}))

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_journey_list(self):
        client = APIClient()
        client.force_authenticate(user=self.reservation_1.user)

        response = client.get(reverse('journey-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

