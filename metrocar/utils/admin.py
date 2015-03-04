from django.contrib import admin
from django.contrib.sites.models import Site

from metrocar.utils import Bunch
from metrocar.utils.models import SiteSettings, EmailTemplate, LogMessage

admin.site.unregister(Site)
admin.site.register(SiteSettings)


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'language')
admin.site.register(EmailTemplate, EmailTemplateAdmin)


class LogMessageAdmin(admin.ModelAdmin):
    list_display = ('created', 'message')
admin.site.register(LogMessage, LogMessageAdmin)


def faux_admin(app_label, module_name, verbose_name=None, **kwargs):
    """
    A class decorator for ModelAdmin classes to create administration
    sections without an actual model.

    Just decorate the ModelAdmin class and it gets automatically registered
    in the desired section, given by `app_label` and `module_name`.
    """
    def faux_admin_decorator(admin_class):
        model = FauxAdminModel(app_label, module_name, verbose_name, **kwargs)
        admin.site.register(model, admin_class)
        return admin_class

    return faux_admin_decorator


def FauxAdminModel(app_label, module_name, verbose_name=None, **kwargs):
    """
    A dummy model with which we can register a ModelAdmin class to Django's
    administration.
    """
    defaults = dict(
        verbose_name=module_name.replace('_', ' ').capitalize(),
        abstract=False,
    )
    attrs = dict(defaults,
        app_label=app_label,
        module_name=module_name,
        **kwargs)
    return []
