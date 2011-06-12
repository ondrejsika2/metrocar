#from django.contrib import admin
from django.contrib.gis import admin

from metrocar.subsidiaries.models import Subsidiary

admin.site.register(Subsidiary)
