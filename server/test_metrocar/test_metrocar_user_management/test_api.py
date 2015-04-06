from datetime import datetime, timedelta
import logging

import django.test
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
import sys
from metrocar import settings

from metrocar.user_management.models import MetrocarUser
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1, create_user_admin_1


class TestReservationsApi(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        MetrocarUser.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        MetrocarUser.objects.all().delete()

    def setUp(self):
        self.user_1 = create_user_1()
        self.user_admin_1 = create_user_admin_1()

    def tearDown(self):
        pass

    def test_perm_1(self):
        client = APIClient()
        response = client.get(reverse('user-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        client = APIClient()
        client.force_authenticate(self.user_admin_1)
        response = client.get(reverse('user-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_detail_user_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.get(
            reverse('user-detail', kwargs={"pk": self.user_1.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_user_failed(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.get(
            reverse('user-detail', kwargs={"pk": self.user_admin_1.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_admin_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.get(
            reverse('user-detail', kwargs={"pk": self.user_1.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_not_exist(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.get(
            reverse('user-detail', kwargs={"pk": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.patch(
            reverse('user-detail', kwargs={"pk": self.user_1.id}),
            data={
                "gender": "F",
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_not_permitted(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.patch(
            reverse('user-detail', kwargs={"pk": self.user_admin_1.id}),
            data={
                "gender": "F",
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_admin_success_1(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.patch(
            reverse('user-detail', kwargs={"pk": self.user_1.id}),
            data={
                "gender": "F",
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_admin_success_2(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.patch(
            reverse('user-detail', kwargs={"pk": self.user_admin_1.id}),
            data={
                "gender": "F",
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_failed_1(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1.user)

        response = client.delete(
            reverse('user-detail', kwargs={"pk": self.user_1.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_failed_2(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1.user)

        response = client.delete(
            reverse('user-detail', kwargs={"pk": self.user_admin_1.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_admin_success_1(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.delete(
            reverse('user-detail', kwargs={"pk": self.user_1.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_admin_success_2(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.delete(
            reverse('user-detail', kwargs={"pk": self.user_admin_1.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user_no_perms(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.post(reverse('user-list'), data={
            "first_name": "Pavel" + str(MetrocarUser.objects.count()),
            "last_name": "Miska",
            "username": 'admin' + str(MetrocarUser.objects.count()),
            "password": 'admin',
            "is_superuser": True,
            "is_staff": True,
            "email": 'pmiska@mailinator.com',
            "drivers_licence_number": '0000000',
            "gender": 'M',
            "identity_card_number": '123123123',
            "primary_phone": '000 000000000',
            "home_subsidiary": 1,
            "invoice_date": datetime.now().strftime('%Y-%m-%d'),
            "language": settings.LANG_CHOICES[0][0],
        })

        # not all required data provided
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_admin_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.post(reverse('user-list'), data={
            "first_name": "Pavel" + str(MetrocarUser.objects.count()),
            "last_name": "Miska",
            "username": 'admin' + str(MetrocarUser.objects.count()),
            "password": 'admin',
            "is_superuser": True,
            "is_staff": True,
            "email": 'pmiska@mailinator.com',
            "drivers_licence_number": '0000000',
            "gender": 'M',
            "identity_card_number": '123123123',
            "primary_phone": '000 000000000',
            "home_subsidiary": 1,
            "invoice_date": datetime.now().strftime('%Y-%m-%d'),
            "language": settings.LANG_CHOICES[0][0],
        })

        # created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            reverse('user-detail', kwargs={"pk": response.data['id']}))

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_admin_no_content(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.post(reverse('user-list'), data={
        })

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_balance_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.get(reverse('userbalance-list'))

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user should have one account balance
        self.assertEqual(len(response.data), 1)

    def test_user_balance_admin(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.get(reverse('userbalance-list'))

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # admin should also have one account balance
        self.assertEqual(len(response.data), 1)

    def test_user_account_history(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.get(reverse('userbalance-list'))

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # admin should also have one account balance
        self.assertEqual(len(response.data), 1)




