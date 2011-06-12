'''
Created on 21.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

"""
Common URL invoice patterns that can be imported to other apps.
"""

urlpatterns = patterns('',
    # invoice printing
    url('(?P<invoice_id>\d+)/%s/$' % slugify(_('print')), 'metrocar.invoices.views.print_invoice', name='metrocar_invoices_print'),
    url('(?P<invoice_id>\d+)/%s/(?P<format>[a-z]+)/$' % slugify(_('print')), 'metrocar.invoices.views.print_invoice', name='metrocar_invoices_print'),
)