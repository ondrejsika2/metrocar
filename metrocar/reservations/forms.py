# #TODO-Vojta remove this file
#
# '''
# Created on 27.3.2010
#
# @author: xaralis
# '''
#
# from django import forms
# from django.utils.translation import gettext_lazy as _
#
# from metrocar.user_management.models import MetrocarUser
# from metrocar.cars.models import Car
# from metrocar.reservations.models import Reservation
#
# CHOICES = [ ( c.id, c.__unicode__() ) for c in Car.objects.all() ]
#
# class ReservationForm(forms.Form):
#     """
#     Form to validate reservation request. Validation is proxied to
#     Reservation.validate() method.
#     """
#     reserved_from = forms.DateTimeField(label=_('Reserved from'),
#         widget=forms.HiddenInput)
#     reserved_until = forms.DateTimeField(label=_('Reserved until'),
#         widget=forms.HiddenInput)
#     car_id = forms.ChoiceField(label=_('Select a car'), choices=CHOICES,
#         widget=forms.HiddenInput)
#     user_id = forms.IntegerField(widget=forms.HiddenInput)
#
#     def clean(self):
#         dt_from = self.cleaned_data.get('reserved_from')
#         dt_till = self.cleaned_data.get('reserved_until')
#         car_id = self.cleaned_data.get('car_id')
#         user_id = self.cleaned_data.get('user_id')
#
#         if dt_from and dt_till and car_id and user_id:
#             car = Car.objects.get(pk=car_id)
#             user = MetrocarUser.objects.get(pk=user_id)
#             val_res, val_errs = Reservation.validate(user, car, dt_from, dt_till)
#
#             if not val_res:
#                 raise forms.ValidationError("\n".join(val_errs))
#
#             return self.cleaned_data
#         else:
#             raise forms.ValidationError(_('Missing some data'))
