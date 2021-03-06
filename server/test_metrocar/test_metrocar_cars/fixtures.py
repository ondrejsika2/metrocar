from datetime import datetime, date, time
from decimal import Decimal
from django.contrib.gis.geos.polygon import Polygon

from metrocar.cars.models import CarModelManufacturer, CarType, Fuel, \
    CarModel, Car, CarColor, Parking, FuelBill
from metrocar.tarification.models import Pricelist, PricelistDay, PricelistDayTime
from test_metrocar.test_metrocar_subsidiaries.fixtures import get_subsidiary
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1, create_account, create_user_admin_1


def create_car_manufacturer_1(save=True):
    car_manufacturer = CarModelManufacturer(
        slug='volkswagen' + str(CarModelManufacturer.objects.all().count()),
        name='Volkswagen'
    )
    if save:
        car_manufacturer.save()
    return car_manufacturer


def create_fuel_1(save=True):
    fuel = Fuel(
        title='diesel' + str(Fuel.objects.all().count())
    )
    if save:
        fuel.save()
    return fuel


def create_car_type_1(save=True):
    car_type = CarType(
        type='Sedan' + str(CarType.objects.all().count())
    )
    if save:
        car_type.save()
    return car_type


def create_car_color_1(save=True):
    car_color = CarColor(
        color="Modra" + str(CarColor.objects.all().count())
    )
    if save:
        car_color.save()
    return car_color

def create_pricelist_1(save=True, car_model=None):
    pricelist = Pricelist(
            available=True,
            name='Test pricelist',
            pickup_fee=100,
            price_per_hour=10,
            price_per_km=50,
            reservation_fee=200,
            valid_from=date(day=1, month=1, year=2000),
            model=car_model
        )
    if save:
        pricelist.save()

    pricelist_day = PricelistDay(
            weekday_from=0,
            pricelist=pricelist
        )
    if save:
        pricelist_day.save()
    pricelist_day_time = PricelistDayTime(
        car_unused_ratio=Decimal('0.5'), car_used_ratio=Decimal('1.6'),
        late_return_ratio=Decimal('5'), time_from=time(hour=0),
        pricelist_day=pricelist_day
    )
    if save:
        pricelist_day_time.save()
    return pricelist


def create_car_model_1(save=True):
    car_model = CarModel(
        engine='engine',
        seats_count=4,
        storage_capacity=100,
        name='Passat',
        type=create_car_type_1(),
        main_fuel=create_fuel_1(),
        manufacturer=create_car_manufacturer_1()
    )
    if save:
        car_model.save()
    return car_model


def create_car_1(save=True):
    car = Car(
        model=create_car_model_1(),
        color=create_car_color_1(),
        owner=create_user_1(),
        home_subsidiary=get_subsidiary(),
        manufacture_date=datetime.now(),
        registration_number="AKD 12-20"
    )
    if save:
        car.save()
    return car


def create_parking_1(save=True):
    parking = Parking(
        name='Karlovo namesti',
        places_count=200,
        land_registry_number='100',
        street='Husova 5',
        city='Praha',
        polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))
        )
    )
    if save:
        parking.save()
    return parking


def create_fuel_bill_1(save=True):
    fuel_bill = FuelBill(
        account=create_user_1().account,
        datetime=datetime.now(),
        money_amount=1000,
        car=create_car_1(),
        fuel=create_fuel_1(),
        liter_count=10,
        place="Praha",
    )
    if save:
        fuel_bill.save()
    return fuel_bill

def create_fuel_bill_2(save=True):
    fuel_bill = FuelBill(
        account=create_user_1().account,
        datetime=datetime.now(),
        money_amount=1500,
        car=create_car_1(),
        fuel=create_fuel_1(),
        liter_count=10,
        place="Praha",
        approved=True,
    )
    if save:
        fuel_bill.save()
    return fuel_bill

def create_fuel_bill_3(save=True):
    fuel_bill = FuelBill(
        account=create_user_admin_1().account,
        datetime=datetime.now(),
        money_amount=2000,
        car=create_car_1(),
        fuel=create_fuel_1(),
        liter_count=10,
        place="Praha",
    )
    if save:
        fuel_bill.save()
    return fuel_bill
