from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from metrocar.reservations.models import Reservation, ReservationReminder, ReservationBill
from metrocar.cars.models import Journey

class JourneyOrderedFormset(BaseInlineFormSet):
    def get_queryset(self):
        return super(BaseInlineFormSet, self).get_queryset().order_by('start_datetime')

class JourneyInline(admin.StackedInline):
    classes = ('collapse-closed',)
    model = Journey
    formset = JourneyOrderedFormset
    exclude = ['user', 'car']
    extra = 0

class ReservationModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'reserved_from', 'reserved_until', 'started', 'ended', 'cancelled', 'price')
    list_filter = ('user', 'car', 'started', 'ended', 'cancelled')
    fieldsets = (
        (_('Basic information'), {'fields': ('user', 'car', 'reserved_from', 'reserved_until', 'started', 'ended', 'cancelled', 'is_service',) }),
        (_('Additional information'), {'fields': ('comment',), 'classes': ('collapse') }),
    )
    inlines = [ JourneyInline, ]
    #readonly_fields = ('started', 'ended')

    def save_formset(self, request, form, formset, change):
        r = form.save(commit=False)
        journeys = formset.save(commit=False)

        # update all available journeys
        if len(journeys) == 0:
            journeys = Journey.objects.filter(reservation=r)

        if len(journeys) != 0 and r.finished != True:
            for journey in journeys:
                journey.reservation = r
                journey.update()
            r.finish()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        reservation = Reservation.objects.get(pk=object_id)
        extra_context = dict(extra_context or {},
            pricing=reservation.get_pricing_summary())
        return super(ReservationModelAdmin, self).change_view(
               request, object_id, form_url, extra_context)


admin.site.register(Reservation, ReservationModelAdmin)
admin.site.register(ReservationReminder)
admin.site.register(ReservationBill)
