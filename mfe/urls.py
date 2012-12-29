from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


# TODO: add namespaces

urlpatterns = patterns('',
    url(r'^%s/' % slugify(_('cars')), include('mfe.cars.urls')),
    url(r'^%s/' % slugify(_('reservations')), include('mfe.reservations.urls')),
    url(r'^%s/' % slugify(_('users')), include('mfe.users.urls')),
    url(r'^', include('mfe.utils.urls')),
    url(r'^%s/' % slugify('invoices'), include('metrocar.invoices.urls.common')),
)

if settings.DEBUG:
    # serving static & media files in development
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
