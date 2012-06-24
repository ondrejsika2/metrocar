'''
Created on 13.3.2010

@author: xaralis
'''

from django import forms
from django.forms.util import ErrorList
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime, timedelta

#from IPython.Shell import IPShellEmbed; IPShellEmbed()()
from metrocar.reservations.forms import CHOICES

from metrocar.user_management.models import MetrocarUser
from metrocar.cars.models import Car, Journey
from metrocar.reservations.models import Reservation
from datetime import datetime, timedelta
from mfe.utils.forms.widgets import *


RESERVATION_TIME_INTERVAL = settings.RESERVATION_TIME_INTERVAL


class ReservationFormOne(forms.Form):

    def __init__(self, data, request, *args, **kwargs):
        super(ReservationFormOne, self).__init__(data, *args, **kwargs)
        # nastaveni vychozich datumu a casu
        from_time, until_time = self.initialize_time(data)

        # pridame na prvni misto widget se zacatkem rezervace
        self.fields.insert(0, 'reserved_from', forms.SplitDateTimeField(label=_('Start time'),
            widget=CalendarSplitDateTimeWidget(widgets=[CalendarDateWidget(),
                                                        CalendarSelectTimeWidget(initTime=from_time)]),
            input_date_formats=[settings.CALENDAR_DATE_FORMAT]))
        # pridame na druhe misto widget s koncem rezervace
        self.fields.insert(1, 'reserved_until', forms.SplitDateTimeField(label=_('End time'),
            widget=CalendarSplitDateTimeWidget(widgets=[CalendarDateWidget(),
                                                        CalendarSelectTimeWidget(initTime=until_time)]),
            input_date_formats=[settings.CALENDAR_DATE_FORMAT]))
        # pridame na treti misto selectbox s automobily
        CARS = [(c.id, c.__unicode__()) for c in Car.list_of_available_cars(from_time, until_time, request.user.home_subsidiary)]
        if len(CARS) == 0:
           CARS = [('0', _('No car is available in chosen time.'))]
        self.fields.insert(2, 'car_id', forms.ChoiceField(label=_('Available cars - select one'), choices=CARS))
        # pridame na ctvrte misto skryte policko s id uzivatele
        self.fields.insert(3, 'user_id', forms.IntegerField(widget=forms.HiddenInput, label=''))

    def create_reservation_time(self, from_time=None, until_time=None):
        if from_time == None and until_time == None:
            now = datetime.now()
            from_time = until_time = self.correct_time(datetime(now.year, now.month, now.day, now.hour, now.minute, 0, 0))
            until_time = until_time + timedelta(minutes=RESERVATION_TIME_INTERVAL)

        return from_time, until_time

    def correct_time(self, time):
        if time.minute % RESERVATION_TIME_SHIFT != 0:
            tmp = time.minute / RESERVATION_TIME_SHIFT
            tmp += 1
            time += timedelta(minutes=((tmp * RESERVATION_TIME_SHIFT) - time.minute))
        else:
            time += timedelta(minutes=RESERVATION_TIME_SHIFT)

        return time

    def initialize_time(self, data):
        if data == None:
            from_time, until_time = self.create_reservation_time()
        else:
            datetime_format = '%d.%m.%Y %H:%M'
            from_time, until_time = self.create_reservation_time(datetime.strptime(data['0-reserved_from_0'] + ' ' + data['0-reserved_from_1'], datetime_format),
                                                                 datetime.strptime(data['0-reserved_until_0'] + ' ' + data['0-reserved_until_1'], datetime_format))

        return from_time, until_time

    def clean(self):
        dt_from = self.cleaned_data.get('reserved_from')
        dt_till = self.cleaned_data.get('reserved_until')
        car_id = self.cleaned_data.get('car_id')
        user_id = self.cleaned_data.get('user_id')

        if dt_from and dt_till and car_id and user_id:
            if car_id == '0':
                raise forms.ValidationError(_('You have to choose any available car'))

            car = Car.objects.get(pk=car_id)
            user = MetrocarUser.objects.get(pk=user_id)
            val_res, val_errs = Reservation.validate(user, car, dt_from, dt_till)

            if not val_res:
                raise forms.ValidationError("\n".join(val_errs))

            return self.cleaned_data
        else:
            raise forms.ValidationError(_('Missing some data'))

class ReservationFormThree(forms.Form):
    """
    Mostly dummy for summary view. Only function is to check if account
    balance is sufficent.
    """
    pass

class AddJourneyForm(forms.ModelForm):

    def __init__(self, data=None, initial=None):
        super(AddJourneyForm, self).__init__(data=data, initial=initial)
        if initial is None:
            initial = data

        start_datetime, end_datetime = self.correct_datetime(initial)
        self.fields['start_datetime'].widget = CalendarSplitDateTimeWidget(widgets=[CalendarDateWidget(),
                                                                                    CalendarSelectTimeWidget(initTime=start_datetime)])
        self.fields['end_datetime'].widget = CalendarSplitDateTimeWidget(widgets=[CalendarDateWidget(),
                                                                                  CalendarSelectTimeWidget(initTime=end_datetime)])

    def clean(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) == 0:
            raise forms.ValidationError(_('Comment can not be empty.'))
        return self.cleaned_data

    def correct_datetime(self, data):
        if data is None:
            return datetime.today(), datetime.today()

        if 'start_datetime' in data and 'end_datetime' in data:
            start_datetime = datetime.strptime(('%s %s' % tuple(data['start_datetime'])), '%d.%m.%Y %H:%M')
            end_datetime = datetime.strptime(('%s %s' % tuple(data['end_datetime'])), '%d.%m.%Y %H:%M')
            return start_datetime, end_datetime
        else:
            start_datetime = datetime.strptime('%s %s' % (data['start_datetime_0'], data['start_datetime_1']), '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime('%s %s' % (data['end_datetime_0'], data['end_datetime_1']), '%Y-%m-%d %H:%M')
            return start_datetime, end_datetime

    class Meta:
        model = Journey
        exclude = ('user', 'car', 'reservation', 'total_price', 'path')
