# -*- coding: utf-8 -*-

'''
Created on 27.3.2010

@author: xaralis
'''

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from metrocar.user_management.models import MetrocarUser

class MetrocarUserCreationForm(forms.Form):
    """
    Form for frontend MetrocarUser creation with all needed validation included.
    """
    username = forms.RegexField(label=_("Username"), max_length=10,
        regex=r'^[\w.@+-]+$', help_text=_("Required. 10 characters or fewer. " 
        "Letters, digits and @/./+/-/_ only."), error_message=_("This value " 
        "may contain only letters, numbers and @/./+/-/_ characters."))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    first_name = forms.RegexField(label=_("First name"), max_length=30,
        regex=u'^[a-zA-ZěščřžýáíéĚŠČŘŽÝÁÍÉ]+$')
    last_name = forms.RegexField(label=_("Last name"), max_length=50,
        regex=u'^[a-zA-ZěščřžýáíéĚŠČŘŽÝÁÍÉ]+$')
    email = forms.EmailField(label=_('E-mail'), max_length=100, help_text=_(""
        "E-mail, where the activation announcment will be send."))
    primary_phone = forms.RegexField(label=_('Telephone number'), max_length=30,
        regex=r'^[0-9]{2,3} [0-9]{9}$', help_text=_("Phone number with "
            "country code in format 123 123456789."))
    secondary_phone = forms.RegexField(label=_('Additional phone'), max_length=30,
        required=False, regex=r'^[0-9]{2,3} [0-9]{9}$', help_text=_("Phone "
            "number with country code in format 123 123456789."))
    date_of_birth = forms.DateField(label=_('Date of birth'), help_text=_('YYYY-MM-DD'))
    drivers_licence_number = forms.RegexField(label=_('Driver licence number'), 
        regex=r'^[A-Z0-9 ]{9}$')
    identity_card_number = forms.RegexField(label=_('Identity card number'),
        regex=r'^[0-9]{9}$')
    language = forms.CharField(label=_('Preferred language'), max_length=2, widget=forms.Select(choices=settings.LANG_CHOICES))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            MetrocarUser.objects.get(username=username)
        except MetrocarUser.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))
    
class MetrocarUserChangeForm(forms.Form):
    """
    Form fo MetrocarUser editation.
    """
    email = forms.EmailField(label=_('E-mail'), max_length=100, help_text=_(""
        "E-mail, where the activation announcment will be send."))
    primary_phone = forms.RegexField(label=_('Telephone number'), max_length=30,
        regex=r'^[0-9]{2,3} [0-9]{9}$', help_text=_("Phone number with "
            "country code in format 123 123456789."))
    secondary_phone = forms.RegexField(label=_('Additional phone'), max_length=30,
        required=False, regex=r'^[0-9]{2,3} [0-9]{9}$', help_text=_("Phone "
            "number with country code in format 123 123456789."))
    language = forms.CharField(label=_('Preferred language'), max_length=2, widget=forms.Select(choices=settings.LANG_CHOICES))
