'''
Created on 11.3.2010

@author: xaralis
'''

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import gettext_lazy as _

import django_tables as tables

from metrocar.cars.models import FuelBill
from metrocar.user_management.models import MetrocarUser, AccountActivity
from metrocar.user_management.forms import MetrocarUserChangeForm
from metrocar.reservations.models import Reservation
from metrocar.invoices.models import Invoice

from forms import MetrocarUserRegistrationForm, AddressChangeForm, FuelBillClaimForm, UsernameForm

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, _('You have been successfully logged in.'))
                if request.POST.has_key('next'):
                    return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(reverse('mfe_users_account'))
            else:
                return render_to_response('users/inactive_account.html',
                    context_instance = RequestContext(request))
        else:
            return render_to_response('users/invalid_credentials.html',
                    context_instance = RequestContext(request))
    else:
        return render_to_response('users/login_required.html', request.GET,
                    context_instance = RequestContext(request))
    
def registration(request):
    if request.user.is_authenticated():
        # get back where you came from
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {}
    if request.method == 'POST':
        form = MetrocarUserRegistrationForm(request.POST)
         
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'primary_phone': form.cleaned_data['primary_phone'],
                'secondary_phone': form.cleaned_data['secondary_phone'],
                'date_of_birth': form.cleaned_data['date_of_birth'],
                'drivers_licence_number': form.cleaned_data['drivers_licence_number'],
                'identity_card_number': form.cleaned_data['identity_card_number'],
                'language': form.cleaned_data['language']
            }
            
            user = MetrocarUser.objects.create_user(username, email, password,**data)
            context['registration_successful'] = True
            messages.success(request, _('You have been successfully registered. You will be sent an e-mail as soon as our administrators validate your registration request.'))
        else:
            messages.error(request, _('Remove errors below.'))
    else:
        form = MetrocarUserRegistrationForm()
    context['form'] = form
    return render_to_response('users/registration.html', context, 
        context_instance = RequestContext(request))
    
@login_required
def detail(request):
    pass
    
@login_required
def account_detail(request):
    user = request.user
    pending_reservations = Reservation.objects.pending().order_by('reserved_from').filter(user=request.user)[:5]
    finished_reservations = Reservation.objects.finished().order_by('-ended').filter(user=request.user)[:5]
    return render_to_response('users/account_detail.html', {
            'pending_reservations': pending_reservations,
            'finished_reservations': finished_reservations,
        }, context_instance=RequestContext(request))
    
@login_required
def account_detail_edit(request):
    from django.core import serializers
    initial = {
        'primary_phone': request.user.primary_phone,
        'secondary_phone': request.user.secondary_phone,
        'email': request.user.email,
        'language': request.user.language,
    }
    if request.method == "POST":
        form = MetrocarUserChangeForm(data=request.POST, initial=initial)
        if form.is_valid():
            request.user.email = form.cleaned_data.get('email')
            request.user.primary_phone = form.cleaned_data.get('primary_phone')
            request.user.secondary_phone = form.cleaned_data.get('secondary_phone')
            request.user.language = form.cleaned_data.get('language')
            request.user.save()
            return HttpResponseRedirect(reverse('mfe_users_account'))
    else:
        form = MetrocarUserChangeForm(initial=initial)
    return render_to_response('users/account_edit.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
@login_required
def account_detail_edit_address(request):
    from metrocar.invoices.models import UserInvoiceAddress
    try:
        address = request.user.invoice_address
    except UserInvoiceAddress.DoesNotExist:
        address = None
    if request.method == "POST":
        form = AddressChangeForm(data=request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('mfe_users_account'))
    else:
        form = AddressChangeForm(instance=address)
    return render_to_response('users/address_edit.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
class AccActivityTable(tables.ModelTable):
    datetime = tables.Column(sortable=True, visible=True)
    as_concrete_class = tables.Column(sortable=False, visible=True)
    money_amount = tables.Column(sortable=True, visible=True)
    account_balance = tables.Column(sortable=True, visible=True) 
    
    class Meta:
        model = AccountActivity
        exclude = ['id', 'account', 'comment', 'content_type']
    
@login_required
def account_activities(request, **kwargs):
    account_act = AccountActivity.objects.filter(account__user=request.user)
    acc_table = AccActivityTable(account_act,
        order_by=request.GET.get('sort', '-datetime'))
    return render_to_response('users/account_activities.html', {
            'table': acc_table
        }, context_instance=RequestContext(request))
    
@login_required
def account_invoices(request):
    context = {
        'invoices': Invoice.objects.filter(user=request.user).order_by('-draw_date'),
        'fuel_bills': FuelBill.objects.filter(account__user=request.user).order_by('-pk')
    }
    return render_to_response('users/invoices.html', context,
        context_instance=RequestContext(request))
    
@login_required
def account_invoices_claim_bill(request):
    if request.method == "POST":
        form = FuelBillClaimForm(request, data=request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.account = request.user.account
            bill.save()
            return render_to_response('users/fuel_bill_added.html', 
                { 'bill': bill }, context_instance=RequestContext(request))
    else:
        form = FuelBillClaimForm(request)
    return render_to_response('users/fuel_bill_form.html', {
        'form': form,
    }, context_instance=RequestContext(request))

# Send email with instructions to reset user passwd
def passwd_reset(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        try:
            user = MetrocarUser.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            messages.error(request, _('User "%s" does not exist.') % request.POST.get('username', None))
            return HttpResponseRedirect('./')
            
        user.request_password_reset()
        messages.info(request, _('Information email was sent on your email address. To set up your new password follow sent instructions.'))
        return HttpResponseRedirect(reverse('mfe_users_login'))
    else:
        form = UsernameForm()
        
    return render_to_response(
        "users/passwd_reset.html", {'form':form},
        context_instance=RequestContext(request)
    )

# Check if hash sent in reset email is valid and let user change his passwd
def passwd_reset_confirm(request, username, unique_hash):
    user = get_object_or_404(MetrocarUser, username=username)
    if unique_hash != user.get_unique_password_reset_hash_string():
        messages.error(request, _('Your URL for password reset is not valid. Check it once more and try again. Remember that your URL is valid only for one day.'))
        return render_to_response(
            "base.html", {},
            context_instance=RequestContext(request)
        )
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Password reset for user "%s" was successful. Now you can log in.') % username)
            return HttpResponseRedirect(reverse('mfe_users_login'))
        else:
            messages.error(request, _('Remove errors below.'))
    else:
        form = SetPasswordForm(None)
        
    return render_to_response(
        "users/passwd_reset_confirm.html", {'form':form},
        context_instance=RequestContext(request)
    )
