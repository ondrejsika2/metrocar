'''
Created on 11.3.2010

@author: xaralis
'''

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as StockFlatPageAdmin

from models import *

class MetaAdmin(admin.ModelAdmin):
    list_display = ('flatpage', 'date_created',)
    list_filter = ('flatpage',)
    ordering = ('flatpage',)
    search_fields = ('flatpage',)

admin.site.register(Meta, MetaAdmin)

class MetaInline(admin.TabularInline):
    model = Meta
    max_num = 1
    extra = 0

class FlatPageAdmin(StockFlatPageAdmin):
    inlines = [ MetaInline ]

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)