#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 12.3.2010

@author: xaralis
'''

from datetime import datetime

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from metrocar.user_management.forms import MetrocarUserCreationForm
from metrocar.invoices.models import UserInvoiceAddress
from metrocar.cars.models import FuelBill, Car

class MetrocarUserRegistrationForm(MetrocarUserCreationForm):
    # moved to init method - specified field position
    #password2 = forms.CharField(label=_("Password confirmation"), 
        #widget=forms.PasswordInput, help_text=_("Enter the same password as "
        #"above, for verification."))
        
    def __init__(self,*args,**kwargs):
        forms.Form.__init__(self,*args,**kwargs)
        self.fields.insert(2,'password2',forms.CharField(label=_("Password confirmation"), 
            widget=forms.PasswordInput, help_text=_("Enter the same password as "
            "above, for verification.")))

    def clean_password2(self):
        password = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
class AddressChangeForm(forms.ModelForm):
    class Meta:
        model = UserInvoiceAddress
        exclude = [ 'deleted', 'user', 'state', ]
        
class FuelBillClaimForm(forms.ModelForm):
    from mfe.utils.forms.widgets import CalendarSplitDateTimeWidget
    datetime = forms.SplitDateTimeField(label='', widget=CalendarSplitDateTimeWidget,
        input_date_formats=[settings.CALENDAR_DATE_FORMAT])
    
    def __init__(self, request, data=None):
        self.request = request
        super(FuelBillClaimForm, self).__init__(data)
    
    class Meta:
        model = FuelBill
        exclude = [ 'approved', 'account', 'account_balance', 'code' ]
        
    def clean_datetime(self):
        """
        We need to check several things:
            - datetime (must be in past)
            - if user was supposed to use the car at the moment
        """
        dt = self.cleaned_data['datetime']
        
        # check if time is in the past
        if dt > datetime.now():
            raise forms.ValidationError(_('Date of claim must be in the past.'))
        return dt
    
    def clean(self):
        cd = self.cleaned_data
        car = cd.get('car')
        datetime = cd.get('datetime')
        # check if the user was allowed to use submitted car in that moment
        if car and datetime:
            if not car.is_user_allowed(self.request.user, datetime):
                raise forms.ValidationError(_('You were not supposed to use '
                    'submitted car in the time you selected.'))
        return cd
    
class UsernameForm(forms.Form):
    username = forms.CharField(max_length=100)
