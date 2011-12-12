'''
Created on 27.2.2010

@author: xaralis
'''

from django.contrib import admin
from django.forms import ModelForm
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from metrocar.tarification.models import *

class PricelistModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'valid_from', 'available', 'deleted')
    list_filter = ('model', 'available', 'deleted')
    fieldsets = (
        (_('Basic information'), { 'fields': ( 'name', 'model', 'valid_from', 'description','available', 'deleted',  ) } ),
        (_('Pricing'), { 'fields': ( 'pickup_fee', 'reservation_fee', 'price_per_hour', 'price_per_km' ) } )
    )
    actions = ['clone_pricelist']

    def change_view(self, request, object_id, extra_content=None):
        summary = Pricelist.objects.get(pk=object_id).get_pricing_summary()
        
        extra_content = {
            'timeline': summary['timeline']  
        }
        return super(PricelistModelAdmin, self).change_view(request, object_id, extra_content)

    def clone_pricelist(self, request, queryset):
        for pricelist in queryset:
            new_pricelist = pricelist.clone()
            new_pricelist.save()
    clone_pricelist.short_description = _("Clone selected")

admin.site.register(Pricelist, PricelistModelAdmin)

class PricelistDayTimeInline(admin.StackedInline):
    classes = ('collapse-open',)
    allow_add = True
    model = PricelistDayTime

class PricelistDayForm(ModelForm):
    class Meta:
        model = PricelistDay
    
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('date') is not None and cleaned_data.get('weekday_from') is not None:
            raise ValidationError(_('Only one of fields "%(date)s" and "%(weekday)s" is allowed.')%{'date': _('Date'), 'weekday': _('Weekday from')})
        return cleaned_data

class PricelistDayModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pricelist', 'date', 'weekday_from', )
    list_filter = ('pricelist', 'weekday_from', )
    form = PricelistDayForm
    inlines = [PricelistDayTimeInline, ]
    
    def change_view(self, request, object_id, extra_content=None):
        pricelist_day = PricelistDay.objects.get(pk=object_id)
        summary = pricelist_day.pricelist.get_pricing_summary()
        
        extra_content = {
            'timeline': summary['timeline'],
            'pricelist_id': pricelist_day.pricelist.pk 
        }
        return super(PricelistDayModelAdmin, self).change_view(
                                                               request, object_id, extra_content
                                                               )

admin.site.register(PricelistDay, PricelistDayModelAdmin)
