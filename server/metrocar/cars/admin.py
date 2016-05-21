from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from metrocar.cars.models import CarModelManufacturer, Car, CarColor, CarType, Fuel, FuelBill, MaintenanceBill, CarModel, Journey, Parking
from metrocar.utils.permissions import PermissionsNameConst as PermName
from metrocar.car_unit_api.models import JourneyDataFile

if settings.GEO_ENABLED:
    from django.contrib.gis import admin
    OSMGeoAdmin = (admin.OSMGeoAdmin
      # FIXME: weird bug on rosti - somehow admin.HAS_OSM == False... (?)
      if admin.HAS_OSM else admin.GeoModelAdmin)
else:
    from django.contrib import admin
    OSMGeoAdmin = admin.ModelAdmin


admin.site.register(CarModelManufacturer)
admin.site.register(CarType)
admin.site.register(CarColor)
admin.site.register(Fuel)


class FuelBillAdmin(admin.ModelAdmin):
    list_display = ('code', 'car', 'fuel', 'liter_count', 'approved')
admin.site.register(FuelBill, FuelBillAdmin)


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'car', 'purpose', 'approved')
admin.site.register(MaintenanceBill, MaintenanceAdmin)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'type', 'engine', 'seats_count', 'storage_capacity')
    list_filter = ('manufacturer', 'type', 'engine',)
admin.site.register(CarModel, CarModelAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'model', 'color', 'last_address', 'active', 'state', 'parking')
    list_filter = ('model', 'color', 'active',)
    fieldsets = (
                 (_('Basic information'), {'fields': ('model', 'registration_number', 'active', 'owner', 'color', 'image', 'home_subsidiary', 'manufacture_date', 'dedicated_parking_only', 'parking')}),
                 )

    def has_delete_permission(self, request, obj=None):
        has_perm = super(CarAdmin, self).has_delete_permission(request, obj)
        if( obj != None ):
            subsidiary = obj.home_subsidiary.name
            perm = self.opts.app_label + "." + PermName.can_delete_car_sub + subsidiary
            has_perm =(has_perm and request.user.has_perm(perm))

        return has_perm

    def save_model(self, request, obj, form, change):
        subsidiary = obj.home_subsidiary.name

        if(change == True):
            perm = self.opts.app_label + "." + PermName.can_change_car_sub + subsidiary
        else:
            perm = self.opts.app_label + "." + PermName.can_add_car_sub + subsidiary

        if not request.user.has_perm(perm):
            raise PermissionDenied

        super(CarAdmin, self).save_model(request, obj, form, change)

admin.site.register(Car, CarAdmin)


class JourneyModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'car',
        'start_datetime',
        'end_datetime',
        'type',
        'length',
        'duration',
        'is_finished',
        'reservation',
        'is_service',
        'total_price',
    )
    list_filter = ('car', 'user', 'type')
    fieldsets = (
        (_('Basic information'), {'fields': (
        'user', 'car', 'reservation', 'start_datetime', 'end_datetime', 'total_price', 'odometer_start',
        'odometer_end'), 'classes': ('show', 'extrapretty',)}),
    )
    ordering = ('start_datetime',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        print "Object id:", object_id

        # import models here to avoid circular reference
        from django.core.exceptions import ObjectDoesNotExist

        # find journey
        try:
            journey = Journey.objects.get(id = object_id)
            is_service = journey.is_service()
            pricing = journey.get_pricing_info()
            print "Journey id:", journey.id
        except ObjectDoesNotExist:
            journey = None
            is_service = None
            pricing = None
            datafile = None
            print "No journey"

        # find datafile
        if journey:
            try:
                datafile = JourneyDataFile.objects.get(journey=object_id)
                print "Datafile id:", datafile.id
            except ObjectDoesNotExist:
                datafile = None
                print "No datafile"

        extra_context = {
            'journey': journey,
            'datafile': datafile,
            'service_journey': is_service,
            'pricing': pricing,
            'filedir': settings.UNIT_DATA_FILES_URL
        }
        return super(JourneyModelAdmin, self).change_view(request, object_id, form_url, extra_context = extra_context)

    # def change_view(self, request, object_id, extra_context=None):
    #     journey = Journey.objects.get(pk=object_id)
    #     pricing = journey.get_pricing_info()
    #
    #
    #     context = {}
    #     context.update(extra_context or {})
    #     context.update({
    #         'journey': journey,
    #         'service_journey': journey.is_service(),
    #         'pricing': pricing
    #     })
    #     return super(JourneyModelAdmin, self).change_view(
    #         request, object_id, context
    #     )


admin.site.register(Journey, JourneyModelAdmin)

class ParkingAdmin(OSMGeoAdmin):
    openlayers_url= "js/openlayers/lib/OpenLayers.js"

admin.site.register(Parking, ParkingAdmin)
