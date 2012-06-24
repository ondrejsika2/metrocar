# -*- coding: utf-8 -*-

'''
Created on 26.3.2010

@author: xaralis
'''
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from datetime import time, datetime


RESERVATION_TIME_SHIFT = settings.RESERVATION_TIME_SHIFT
RESERVATION_TIME_INTERVAL = settings.RESERVATION_TIME_INTERVAL


class CalendarDateWidget(forms.DateTimeInput):
    format = getattr(settings, 'CALENDAR_DATE_FORMAT', '%d.%m.%Y')

    def __init__(self, attrs={}, format=None, initDate=datetime.today()):
        super(CalendarDateWidget, self).__init__(
            attrs={'class': 'datepicker', 'size': '10', 'value': initDate.strftime('%-d.%-m.%Y'), 'maxlength' : '10'}, format=format)

class CalendarTimeWidget(forms.TimeInput):
    format = getattr(settings, 'CALENDAR_TIME_FORMAT', '%H:%M')

    def __init__(self, attrs={}, format=None):
        super(CalendarTimeWidget, self).__init__(
            attrs={'class': 'timepicker', 'size': '10'}, format=format)

'''
Widget with select input element for time
'''
class CalendarSelectTimeWidget(forms.Select):
    format = getattr(settings, 'CALENDAR_TIME_FORMAT', '%H:%M')

    '''
    Metoda naplni rolovatka s casem od pulnoci do pulnoci po ctvrt hodine
    '''
    def __init__(self, attrs={}, format=None, initTime=datetime.today()):
        TIMES = []
        self.initTime = initTime

        for hour in range(0, 24):
            for minute in range(0, 60, RESERVATION_TIME_SHIFT):
                t = time(hour, minute).strftime('%H:%M')
                TIMES.append([t, t])
        super(CalendarSelectTimeWidget, self).__init__(attrs=attrs, choices=TIMES)

    def render(self, name, value, attrs=None, choices=()):
        return super(CalendarSelectTimeWidget, self).render(name, self.initTime.strftime('%H:%M'), attrs, choices)

class CalendarSplitDateTimeWidget(forms.SplitDateTimeWidget):
    date_format = getattr(settings, 'CALENDAR_DATE_FORMAT', '%d.%m.%Y')
    time_format = getattr(settings, 'CALENDAR_TIME_FORMAT', '%H:%M')

    def __init__(self, attrs=None, widgets=[]):
        if widgets == []:
            widgets = [CalendarDateWidget, CalendarTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u"%s %s %s %s" % (u'Datum',
            rendered_widgets[0], u'Čas', rendered_widgets[1]))
