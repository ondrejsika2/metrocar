from functools import wraps

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from metrocar.audit import views
from metrocar.utils.admin import faux_admin


NO = lambda *args, **kwargs: False


def wrap(model_admin, view):
    """
    Wrap a view for a `model_admin` instance to check for permissions.

    `model_admin` should provide a ``has_permission(user)`` method that
    will return whether a given user has a permission to access `view`.
    """
    @wraps(view)
    def decorated(request, *args, **kwargs):
        if model_admin.has_permission(request.user):
            return view(request, *args, **kwargs)
        return HttpResponseForbidden()
    return model_admin.admin_site.admin_view(decorated)


@faux_admin('audit', 'car_positions')
class CarPositionsAdmin(admin.ModelAdmin):

    def get_urls(self):
        index = wrap(self, views.CarPositionsMap.as_view())
        data = wrap(self, csrf_exempt(views.CarPositions.as_view()))
        return patterns('',
            url(r'^data/$', data, name='car_positions_data'),

            # needed for admin
            url(r'^', index, name='%s_%s_changelist' % (
                self.model._meta.app_label,
                self.model._meta.module_name)),

            # url alias / shortcut
            url(r'^', index, name='car_positions'),
        )

    has_add_permission = NO
    has_delete_permission = NO

    def has_permission(self, user):
        """
        Return whether `user` should be allowed to view car positions.
        """
        return user.is_superuser

    def has_change_permission(self, request, obj=None, *args, **kwargs):
        return self.has_permission(request.user)


@faux_admin('audit', 'usage_history')
class UsageHistoryAdmin(admin.ModelAdmin):

    def get_urls(self):
        index = wrap(self, views.UsageHistory.as_view())
        query = wrap(self, csrf_exempt(views.Query.as_view()))
        return patterns('',
            url(r'^query/$', query, name='usage_history_query'),

            # needed for admin
            url(r'^', index, name='%s_%s_changelist' % (
                self.model._meta.app_label,
                self.model._meta.module_name)),

            # url alias / shortcut
            url(r'^', index, name='usage_history'),
        )

    has_add_permission = NO
    has_delete_permission = NO

    def has_permission(self, user):
        """
        Return whether `user` should be allowed to view usage history.
        """
        return user.is_superuser

    def has_change_permission(self, request, obj=None, *args, **kwargs):
        return self.has_permission(request.user)
