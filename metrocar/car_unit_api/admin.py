from django.contrib import admin

from smartadmin import SmartAdmin

from metrocar.car_unit_api.models import CarUnit


admin.site.register(CarUnit, SmartAdmin)
