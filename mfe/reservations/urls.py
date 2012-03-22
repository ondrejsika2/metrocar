'''
Created on 11.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

urlpatterns = patterns('',
    # reservation creation
    url('^$', 'mfe.reservations.views.reservation', name='mfe_reservations_reservation'),
    url('^%s/(?P<car_id>\d+)/$' % slugify(_('reserve car')), 'mfe.reservations.views.reservation', name='mfe_reservations_reserve_car'),
    url('^%s/$' % slugify(_('success')), 'django.views.generic.simple.direct_to_template', { 'template': 'reservations/reservation/success.html' }, name='mfe_reservations_reservation_success'),
    url(r'^recount_price_estimation/$','mfe.reservations.views.recount_price_estimation', name='mfe_reservations_recount_price_estimation'),

    # reservation cancel
    url('^(?P<reservation_id>\d+)/%s/$' % slugify(_('submit-cancel')), 'mfe.reservations.views.cancel_reservation', name='mfe_reservations_submit_cancel_reservation'),
    url('^(?P<reservation_id>\d+)/%s/$' % slugify(_('cancel')), 'mfe.reservations.views.cancel_reservation', {'confirmed':True}, name='mfe_reservations_cancel_reservation'),

    # reservation edit
    url('^(?P<reservation_id>\d+)/%s/$' % slugify(_('edit')), 'mfe.reservations.views.edit_reservation', name='mfe_reservations_edit_reservation'),

    # record journey
    url('^%s/$' % slugify(_('oustanding loans')), 'mfe.reservations.views.outstanding_loans', name='mfe_reservations_outstanding_loans'),
    url('^(?P<reservation_id>\d+)/%s/$' % slugify(_('add journey')), 'mfe.reservations.views.add_journey', name='mfe_reservations_add_journey'),
    url('^%s/(?P<journey_id>\d+)/$' % slugify(_('delete journey')), 'mfe.reservations.views.delete_journey', name='mfe_reservations_delete_journey'),
    url('^(?P<reservation_id>\d+)/%s/$' % slugify(_('finish reservation')), 'mfe.reservations.views.finish_reservation', name='mfe_reservations_finish_reservation'),
)
