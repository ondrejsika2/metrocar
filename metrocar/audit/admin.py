from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from metrocar.utils import Bunch
from metrocar.audit import views


NO = lambda *args, **kwargs: False


class UsageHistoryAdmin(admin.ModelAdmin):

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        index = self.admin_site.admin_view(views.UsageHistory.as_view())
        return patterns('',
            url(r'^query/$', views.Query.as_view(), name='usage_history_query'),
            url(r'^', index, name='%s_%s_changelist' % info),  # needed for admin
            url(r'^', index, name='usage_history'),  # url alias / shortcut
        )

    has_add_permission = NO
    has_delete_permission = NO

    def has_change_permission(self, request, obj=None, *args, **kwargs):
        # TODO: permissions ?
        if request.user.is_superuser:
            return True
        else:
            return False


def FauxAdmin(module_name, verbose_name=None, **kwargs):
    defaults = dict(
        app_label='audit',
        verbose_name=module_name.replace('_', ' ').capitalize(),
        abstract=False,
    )
    attrs = dict(defaults, module_name=module_name, **kwargs)
    return [Bunch(_meta=Bunch(
        verbose_name_plural=attrs['verbose_name'], **attrs))]


admin.site.register(FauxAdmin('usage_history'), UsageHistoryAdmin)
