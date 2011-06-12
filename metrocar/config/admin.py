'''
Created on 8.3.2010

@author: xaralis
'''

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from grappelli.sites import GrappelliSite

admin.site = GrappelliSite()
admin.autodiscover()

admin.site.groups = {
    0: {
        'name': _('Metrocar user management'),
        'apps': [ 'user_management' ]
    },
    1: {
        'name': _('Django user management'),
        'apps': [ 'auth' ]
    },
    2: {
        'name': _('Car pool'),
        'apps': [ 'cars', 'car_unit_management' ]
    },
    3: {
        'name': _('Reservations'),
        'apps': [ 'reservations' ]
    },
    4: {
        'name': _('Invoices'),
        'apps': [ 'invoices' ]
    },
    5: {
        'name': _('Tarification'),
        'apps': [ 'tarification', 'tariffs' ]
    },
    6: {
        'name': _('Utils'),
        'apps': [ 'flatpages', 'flatpagesmeta', 'subsidiaries', 'utils' ]
    },
    7: {
        'name': _('System settings'),
        'apps': [ 'django_evolution', 'grappelli' ],
    }
}

admin.site.collections = {
    0: {
        'title': _('User mangement'),
        'groups': [ 0, 1, 4 ]
    },
    1: {
        'title': _('Reservations/Tarification'),
        'groups': [ 3, 5 ]
    }
}