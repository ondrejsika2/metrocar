'''
Created on 11.3.2010

@author: xaralis
'''

from django.conf.urls.defaults import *
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.views import logout

urlpatterns = patterns('',
    # user account
    url('%s/$' % slugify(_('my account')), 'mfe.users.views.account_detail', name='mfe_users_account'),
    url('%s/%s/$' % (slugify(_('my account')), slugify(_('account activities'))), 'mfe.users.views.account_activities', name='mfe_users_account_activities'),
    
    # user detail
    url('%s/(?P<id>\d+)/$' % slugify(_('user')), 'mfe.users.views.detail', name='mfe_users_detail'),
    
    # change password
    url('%s/$' % slugify(_('change password')), 'django.contrib.auth.views.password_change', { 'template_name': 'users/password_change.html' }, name='mfe_users_change_password'),
    url('%s/$' % slugify(_('password changed')), 'django.contrib.auth.views.password_change_done', { 'template_name': 'users/password_change_done.html' }, name='mfe_users_change_password_done'),
    
    # forgotten password
    url('%s/$' % slugify(_('password reset')), 'mfe.users.views.passwd_reset', name='mfe_users_passwd_reset'),
    url('%s/(?P<username>\w+)/(?P<unique_hash>.+)/$' % slugify(_('password reset')), 'mfe.users.views.passwd_reset_confirm', name='mfe_users_passwd_reset_confirm'),
    
    # user detail edit
    url('%s/%s/$' % (slugify(_('my account')), slugify(_('edit'))), 'mfe.users.views.account_detail_edit', name='mfe_users_account_edit'),
    
    # address edit
    url('%s/%s/$' % (slugify(_('my account')), slugify(_('edit address'))), 'mfe.users.views.account_detail_edit_address', name='mfe_users_account_edit_address'),
    
    # invoices, bills
    url('%s/%s/$' % (slugify(_('my account')), slugify(_('invoices and bills'))), 'mfe.users.views.account_invoices', name='mfe_users_account_invoices_and_bills'),
    url('%s/%s/%s/$' % (slugify(_('my account')), slugify(_('invoices and bills')), slugify(_('claim new fuel bill'))), 'mfe.users.views.account_invoices_claim_bill', name='mfe_users_account_invoices_and_bills_claim_bill'),
    url('%s/%s/%s/$' % (slugify(_('my account')), slugify(_('invoices and bills')), slugify(_('transfer money'))), 'mfe.users.views.account_invoices_transfer_money', name='mfe_users_account_invoices_and_bills_transfer_money'),
    
    # RESERVATIONS URLS
    # pending reservations list
    url('^%s/$' % slugify(_('pending')), 'mfe.reservations.views.PendingList', name='mfe_reservations_pending_list'),
    url('^%s/%s/(?P<page>\d+)/$' % (slugify(_('pending')), slugify(_('page'))), 'mfe.reservations.views.PendingList', name='mfe_reservations_pending_list'),
    
    # finished reservations list
    url('^%s/$' % slugify(_('finished')), 'mfe.reservations.views.FinishedList', name='mfe_reservations_finished_list'),
    url('^%s/%s/(?P<page>\d+)/$' % (slugify(_('pending')), slugify(_('page'))), 'mfe.reservations.views.FinishedList', name='mfe_reservations_finished_list'),
)
