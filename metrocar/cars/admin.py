from datetime import datetime

from django.conf.urls.defaults import patterns
from django.contrib import messages
from django.contrib.gis import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from metrocar.cars import utils
from metrocar.cars.models import *
from metrocar.utils.permissions import PermissionsNameConst as PermName

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

class CarAdmin(admin.OSMGeoAdmin):
    list_display = ('registration_number', 'model', 'color', 'last_echo', 'last_address', 'active', 'state',)
    list_filter = ('model', 'color', 'active',)
    fieldsets = (
                 (_('Basic information'), {'fields': ('model', 'registration_number', 'active', 'owner', 'color', 'image', 'home_subsidiary', 'manufacture_date', 'dedicated_parking_only', )}),
                 (_('Connection information'), {'fields': ('imei', 'authorization_key', 'last_echo', 'mobile_number', )}),
                 (_('Location'), {'fields': ('last_position', )})
                 )
    
    def changelist_view(self, request, extra_context=None):
        map = utils.get_car_infomap()
        return super(CarAdmin, self).changelist_view(request, {'car_position_map': map})
    
    def change_auth_key(self, request, object_id, extra_context=None):
        from metrocar.cars.forms import SetCarAuthKeyForm
        car = Car.objects.get(pk=object_id)
        
        if request.method == 'POST':
            form = SetCarAuthKeyForm(car, request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Authorization key changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = SetCarAuthKeyForm(car)
        return render_to_response('admin/cars/car/change_auth_key.html',
                                  {
                                  'title': _('Change authorization key for %s') % car.get_full_name(),
                                  'form': form,
                                  'is_popup': '_popup' in request.REQUEST,
                                  'add': True,
                                  'change': False,
                                  'has_delete_permission': False,
                                  'has_change_permission': True,
                                  'has_absolute_url': False,
                                  'opts': car._meta,
                                  'original': car,
                                  'save_as': False,
                                  'show_save': True,
                                  },
                                  context_instance=RequestContext(request))
    
    def get_urls(self):
        urls = super(CarAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/change-authorization-key/$',
                           self.admin_site.admin_view(self.change_auth_key))
                           )
        return my_urls + urls

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

class CarPositionInline(admin.StackedInline):
    classes = ('collapse-closed',)
    model = CarPosition

class JourneyModelAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'user', 'car', 'start_datetime', 'end_datetime', 'type', 'length', 'is_finished', 'reservation', 'is_service', 'total_price',)
    list_filter = ('car', 'user', 'type')
    fieldsets = (
                 (_('Basic information'), {'fields': ('user', 'car', 'reservation', 'start_datetime', 'end_datetime', 'total_price', 'speedometer_start', 'speedometer_end'), 'classes': ('show', 'extrapretty',)}),
                 (_('Track'), {'fields': ('path',), 'classes': ('wide',)}),
                 )
    inlines = [
        CarPositionInline,
    ]
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
    
class CarPositionModelAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'journey', 'get_sequence_nr',)
    list_filter = ('journey',)

admin.site.register(Journey, JourneyModelAdmin)
admin.site.register(Parking, admin.OSMGeoAdmin)
admin.site.register(CarPosition, CarPositionModelAdmin)
