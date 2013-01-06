from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from metrocar.cars.models import CarModelManufacturer, Car, CarColor, CarType, Fuel, FuelBill, ParkingDescription, MaintenanceBill, CarModel, Journey, Parking
from metrocar.utils.permissions import PermissionsNameConst as PermName

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
admin.site.register(ParkingDescription)


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
    list_display = ('registration_number', 'model', 'color', 'last_address', 'active', 'state',)
    list_filter = ('model', 'color', 'active',)
    fieldsets = (
                 (_('Basic information'), {'fields': ('model', 'registration_number', 'active', 'owner', 'color', 'image', 'home_subsidiary', 'manufacture_date', 'dedicated_parking_only', )}),
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
    list_display = ('id', 'user', 'car', 'start_datetime', 'end_datetime', 'type', 'length', 'is_finished', 'reservation', 'is_service', 'total_price',)
    list_filter = ('car', 'user', 'type')
    fieldsets = (
                 (_('Basic information'), {'fields': ('user', 'car', 'reservation', 'start_datetime', 'end_datetime', 'total_price', 'speedometer_start', 'speedometer_end'), 'classes': ('show', 'extrapretty',)}),
                 )
    ordering = ('start_datetime',)

    def change_view(self, request, object_id, extra_content=None):
        journey = Journey.objects.get(pk=object_id)
        pricing = journey.get_pricing_info()
        extra_content = {
            'service_journey': journey.is_service(),
            'pricing': pricing
        }
        return super(JourneyModelAdmin, self).change_view(
                                                          request, object_id, extra_content
                                                          )


admin.site.register(Journey, JourneyModelAdmin)
admin.site.register(Parking, OSMGeoAdmin)
