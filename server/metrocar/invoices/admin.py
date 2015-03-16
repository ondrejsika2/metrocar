from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from metrocar.invoices.models import *

class InvoiceItemInline(admin.StackedInline):
    model = InvoiceItem
    classes = ('collapse-closed',)
    max_num = 1

class InvoiceModelAdmin(admin.ModelAdmin):    
    inlines = [ InvoiceItemInline, ]    
    fieldsets = (
        (_('Basic information'), { 'fields': ( 'user', 'draw_date', 'due_date',  ) } ),
    )

admin.site.register(Invoice, InvoiceModelAdmin)
admin.site.register(InvoiceItem)
admin.site.register(UserInvoiceAddress)
admin.site.register(CompanyInvoiceAddress)
admin.site.register(PaymentMethod)