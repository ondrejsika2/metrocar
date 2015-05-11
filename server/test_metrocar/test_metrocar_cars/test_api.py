from datetime import datetime, timedelta
import os
import django.test
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from metrocar.cars.models import Reservation, Car, FuelBill
from metrocar.user_management.models import MetrocarUser, Account
from test_metrocar.test_metrocar_cars.fixtures import create_car_1, create_car_model_1, create_car_color_1, \
    create_fuel_bill_1, create_fuel_bill_2, create_fuel_bill_3
from test_metrocar.test_metrocar_subsidiaries.fixtures import get_subsidiary
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1, create_user_admin_1


class TestCarApi(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        Car.objects.all().delete()
        MetrocarUser.objects.all().delete()
        Account.objects.all().delete()
        FuelBill.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        Car.objects.all().delete()
        MetrocarUser.objects.all().delete()

    def setUp(self):
        self.car_1 = create_car_1()
        self.user_1 = create_user_1()
        self.user_admin_1 = create_user_admin_1()

    def tearDown(self):
        MetrocarUser.objects.all().delete()

    def test_list(self):
        client = APIClient()
        response = client.get(reverse('car-list'))

        print response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_detail_success(self):
        client = APIClient()

        response = client.get(
            reverse('car-detail', kwargs={"pk": self.car_1.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_not_exist(self):
        client = APIClient()

        response = client.get(
            reverse('car-detail', kwargs={"pk": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_not_permitted(self):
        client = APIClient()
        client.force_authenticate(create_user_1())

        response = client.patch(
            reverse('car-detail', kwargs={"pk": self.car_1.id}),
            data={
                "manufacture_date": datetime.now(),
            })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.patch(
            reverse('car-detail', kwargs={"pk": self.car_1.id}),
            data={
                "manufacture_date": datetime.now(),
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_not_exist(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.patch(
            reverse('car-detail', kwargs={"pk": 9999}),
            data={
                "manufacture_date": datetime.now(),
            })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_permitted(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.delete(
            reverse('car-detail', kwargs={"pk": self.car_1.id}))

        # deleted
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_success(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.delete(
            reverse('car-detail', kwargs={"pk": self.car_1.id}))

        # deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(
            reverse('car-detail', kwargs={"pk": self.car_1.id}))

        # make sure if it is deleted
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_no_perms(self):
        car_model_1 = create_car_model_1()
        car_color_1 = create_car_color_1()
        home_subsidiary = get_subsidiary()

        client = APIClient()
        client.force_authenticate(user=self.user_1)

        response = client.post(reverse('car-list'), data={
            "model": car_model_1.id,
            "color": car_color_1.id,
            "owner": self.user_1.id,
            "home_subsidiary": home_subsidiary.id,
            "manufacture_date": datetime.now(),
            "registration_number": "AKD 12-20"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_no_content(self):
        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.post(reverse('car-list'), data={})

        # not all required data provided
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_success(self):
        car_model_1 = create_car_model_1()
        car_color_1 = create_car_color_1()
        home_subsidiary = get_subsidiary()

        client = APIClient()
        client.force_authenticate(user=self.user_admin_1)

        response = client.post(reverse('car-list'), data={
            "model": car_model_1.id,
            "color": car_color_1.id,
            "owner": self.user_admin_1.id,
            "home_subsidiary": home_subsidiary.id,
            "manufacture_date": datetime.now(),
            "registration_number": "AKD 12-20"
        })

        # created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            reverse('car-detail', kwargs={"pk": response.data['id']}))

        # make sure if it is saved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_car_fuel_bill_user_list(self):
        car_fuel_bill_1 = create_fuel_bill_1()
        car_fuel_bill_2 = create_fuel_bill_2()
        car_fuel_bill_3 = create_fuel_bill_3()

        client = APIClient()
        client.force_authenticate(user=car_fuel_bill_1.account.user)

        response = client.get(reverse('fuelbill-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user gets just his fuel bills
        self.assertEqual(len(response.data), 2)

    def test_car_fuel_bill_user_create(self):
        car_fuel_bill_1 = create_fuel_bill_1(False)

        client = APIClient()
        client.force_authenticate(user=car_fuel_bill_1.account.user)

        with open("{}/{}".format(os.path.dirname(__file__), 'test-file.jpg'), "rb") as fl:
            fl.seek(0)
            response = client.post(reverse('fuelbill-list'), data={
                "account": car_fuel_bill_1.account.id,
                "datetime": car_fuel_bill_1.datetime,
                "money_amount": car_fuel_bill_1.money_amount,
                "car": car_fuel_bill_1.car.id,
                "fuel": car_fuel_bill_1.fuel.id,
                "liter_count": car_fuel_bill_1.liter_count,
                "place": car_fuel_bill_1.place,
                "image": fl,
            }, format='multipart')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_car_fuel_bill_user_changes_of_approved_failed(self):
        car_fuel_bill_1 = create_fuel_bill_1(False)

        client = APIClient()
        client.force_authenticate(user=car_fuel_bill_1.account.user)

        response = client.post(reverse('fuelbill-list'), data = {
            "account": car_fuel_bill_1.account.id,
            "datetime": car_fuel_bill_1.datetime,
            "money_amount": car_fuel_bill_1.money_amount,
            "car": car_fuel_bill_1.car.id,
            "fuel": car_fuel_bill_1.fuel.id,
            "liter_count": car_fuel_bill_1.liter_count,
            "place": car_fuel_bill_1.place,
            "approved": True,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





