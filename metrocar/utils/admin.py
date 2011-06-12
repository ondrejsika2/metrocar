__author__="Xaralis"
__date__ ="$28.10.2009 17:35:10$"

from django.contrib import admin
from django.contrib.sites.models import Site

from metrocar.utils.models import SiteSettings, EmailTemplate, LogMessage

admin.site.unregister(Site)
admin.site.register(SiteSettings)

class EmailTemplateAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'language')
admin.site.register(EmailTemplate, EmailTemplateAdmin)

class LogMessageAdmin(admin.ModelAdmin):
    	list_display = ('created', 'message')
admin.site.register(LogMessage, LogMessageAdmin)