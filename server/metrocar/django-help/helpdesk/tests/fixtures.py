#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from metrocar.user_management.models import MetrocarUser

def create_admin_only():
    user = MetrocarUser(
        first_name="admin_firstname" + str(MetrocarUser.objects.count()),
        last_name="second_name",
        username="admin" + str(MetrocarUser.objects.count()),
        password="password",
        email='admin@localhost.com',
        drivers_licence_number='123123123',
        gender='M',
        identity_card_number='123123123',
        primary_phone='420 123456789',
        language=settings.LANGUAGES[0][0],
        is_superuser = True,
    )
    user.save()
    return user

def create_technician_only():
    user = MetrocarUser(
        first_name="technician_firstname" + str(MetrocarUser.objects.count()),
        last_name="technician_name",
        username="technician" + str(MetrocarUser.objects.count()),
        password="password",
        email='technician@localhost.com',
        drivers_licence_number='123123123',
        gender='M',
        identity_card_number='123123123',
        primary_phone='420 123456789',
        language=settings.LANGUAGES[0][0],
        is_staff = True,
    )
    user.save()
    return user
