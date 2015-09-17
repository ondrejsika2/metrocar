#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from metrocar.user_management.models import MetrocarUser

# creating users
def create_admin_only():
    user = MetrocarUser(
        first_name="admin_firstname" + str(MetrocarUser.objects.count()),
        last_name="admin_lastname",
        username="administr" + str(MetrocarUser.objects.count()),
        password="passworda",
        email='administr@localhost.com',
        drivers_licence_number='123123123',
        gender='M',
        identity_card_number='123123123',
        primary_phone='420 111111111',
        language=settings.LANGUAGES[0][0], # CZ
    )
    user.is_superuser = True
    user.save()
    return user
    
def create_customer_only():
    user = MetrocarUser(
        first_name="customer_firstname" + str(MetrocarUser.objects.count()),
        last_name="customer_lastname",
        username="customer" + str(MetrocarUser.objects.count()),
        password="password",
        email='customer@localhost.com',
        drivers_licence_number='123123123',
        gender='M',
        identity_card_number='123123123',
        primary_phone='420 111111111',
        language=settings.LANGUAGES[0][0],
        is_active=True,
    )
    user.save()
    return user    

def create_technician_only():
    user = MetrocarUser(
        first_name="technician_firstname" + str(MetrocarUser.objects.count()),
        last_name="technician_lastname",
        username="technician" + str(MetrocarUser.objects.count()),
        password="password",
        email='technician@localhost.com',
        drivers_licence_number='123123123',
        gender='M',
        identity_card_number='123123123',
        primary_phone='420 555555555',
        language=settings.LANGUAGES[0][0],
        is_staff = True,
    )
    user.save()
    return user
    
# ----------------------------------------------------------------------------------------------
# creating tickets, queues
from metrocar.helpdesk.models import Queue, Ticket
def create_queue():
	queue = Queue(title="Queue_title_" + str(Queue.objects.count()), slug="Queue_slug_" + str(Queue.objects.count()))
	queue.save()
	return queue

def create_ticket(p_queue):
	t = Ticket(title="Ticket_title_" + str(Ticket.objects.count()), queue=p_queue, description="Ticket_description_" + str(Ticket.objects.count()))
	t.save()
	return t

    
    
# ----------------------------------------------------------------------------------------------
# creating reservations
from datetime import datetime, timedelta
from metrocar.reservations.models import Reservation
def create_reservation(p_user, p_car):
    return Reservation.objects.get_or_create(
        reserved_from=(datetime.now() + timedelta(hours=10)),reserved_until=(datetime.now() + timedelta(hours=20)),user=p_user,car=p_car
    )[0]
# ----------------------------------------------------------------------------------------------	
# creating cars and connected classes
# inspired in Metrocar test suite
from metrocar.cars.models import CarModelManufacturer, CarType, Fuel, CarModel, Car, CarColor, Parking
from metrocar.subsidiaries.models import Subsidiary

def create_owner(save=True):
    user = MetrocarUser(
        first_name="owner_firstname" + str(MetrocarUser.objects.count()),
        last_name="owner_lastname",
        username="owner" + str(MetrocarUser.objects.count()),
        password="password",
        email='owner@localhost.com',
        drivers_licence_number='123123123',
        gender='M',
        identity_card_number='123123123',
        primary_phone='420 555555555',
        language=settings.LANGUAGES[0][0],
        is_staff = True,
    )
    if save:
        user.save()
    return user

def create_car_manufacturer(save=True):
    car_manufacturer = CarModelManufacturer(
        slug='skoda' + str(CarModelManufacturer.objects.all().count()),
        name='Skoda'
    )
    if save:
        car_manufacturer.save()
    return car_manufacturer


def create_fuel(save=True):
    fuel = Fuel(
        title='diesel' + str(Fuel.objects.all().count())
    )
    if save:
        fuel.save()
    return fuel


def create_car_type(save=True):
    car_type = CarType(
        type='Combi' + str(CarType.objects.all().count())
    )
    if save:
        car_type.save()
    return car_type


def create_car_color(save=True):
    car_color = CarColor(
        color="Blue" + str(CarColor.objects.all().count())
    )
    if save:
        car_color.save()
    return car_color


def create_car_model(save=True):
    car_model = CarModel(
        engine='engine',
        seats_count=4,
        storage_capacity=100,
        name='car_model_name',
        type=create_car_type(),
        main_fuel=create_fuel(),
        manufacturer=create_car_manufacturer()
    )
    if save:
        car_model.save()
    return car_model


def create_car(save=True):
    car = Car(
        model=create_car_model(),
        color=create_car_color(),
        owner=create_owner(),
        home_subsidiary=Subsidiary.objects.get_current(),
        manufacture_date=datetime.now(),
        registration_number=str(Car.objects.all().count())
    )
    if save:
        car.save()
    return car
# ----------------------------------------------------------------------------------------------	
