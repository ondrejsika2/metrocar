from django.contrib import admin
from metrocar.tariffs.models import *

admin.site.register(FixedPaymentTariff)
admin.site.register(FixedPaymentTariffHistory)
