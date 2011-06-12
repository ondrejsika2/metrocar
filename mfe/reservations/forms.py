'''
Created on 13.3.2010

@author: xaralis
'''

from django import forms
from django.utils.translation import gettext_lazy as _

from metrocar.reservations.forms import CHOICES

class ReservationFormOne(forms.Form):
    car_id = forms.ChoiceField(label=_('Select a car'), choices=CHOICES)
    
class ReservationFormThree(forms.Form):
    """
    Mostly dummy for summary view. Only function is to check if account 
    balance is sufficent.
    """
    pass
        