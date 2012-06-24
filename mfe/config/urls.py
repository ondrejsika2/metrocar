from django.conf.urls.defaults import *
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

urlpatterns = patterns('',
    # cars includes
    url(r'^%s/' % slugify(_('cars')), include('mfe.cars.urls')),
    # reservations includes
    url(r'^%s/' % slugify(_('reservations')), include('mfe.reservations.urls')),
    # users includes
    url(r'^%s/' % slugify(_('users')), include('mfe.users.urls')),
    # service includes
    url(r'^', include('mfe.utils.urls')),
    # metrocar baseproj includes
    url(r'^%s/' % slugify('invoices'), include('metrocar.invoices.urls.common')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
