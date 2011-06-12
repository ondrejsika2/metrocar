from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet

from metrocar.reservations.models import *
from metrocar.cars.models import Journey

class JourneyOrderedFormset(BaseInlineFormSet):
    def get_queryset(self):
        return super(BaseInlineFormSet, self).get_queryset().order_by('start_datetime')

class JourneyInline(admin.StackedInline):
    classes = ('collapse-closed',)
    model = Journey
    formset = JourneyOrderedFormset

class ReservationModelAdmin(admin.OSMGeoAdmin):
    list_display = ('user', 'car', 'reserved_from', 'reserved_until', 'started', 'ended', 'cancelled', 'price')
    list_filter = ('user', 'car', 'started', 'ended', 'cancelled')
    fieldsets = (
        (_('Basic information'), {'fields': ('user', 'car', 'reserved_from', 'reserved_until', 'started', 'ended', 'cancelled', 'is_service',) }),
        (_('Additional information'), {'fields': ('comment',), 'classes': ('collapse') }),
        (_('Track'), {'fields': ('path',), 'classes': ('wide') }),
    )
    inlines = [ JourneyInline, ]
    #readonly_fields = ('started', 'ended')
    
    def change_view(self, request, object_id, extra_content=None):
        reservation = Reservation.objects.get(pk=object_id)
        extra_content = {
            'pricing': reservation.get_pricing_summary()
        }
        return super(ReservationModelAdmin, self).change_view(
               request, object_id, extra_content
        )

admin.site.register(Reservation, ReservationModelAdmin)
admin.site.register(ReservationReminder)
admin.site.register(ReservationBill)
