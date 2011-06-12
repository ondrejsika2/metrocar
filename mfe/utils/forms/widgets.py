# -*- coding: utf-8 -*-

'''
Created on 26.3.2010

@author: xaralis
'''
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

class CalendarDateWidget(forms.DateTimeInput):
    format = getattr(settings, 'CALENDAR_DATE_FORMAT', '%d.%m.%Y')

    def __init__(self, attrs={}, format=None):
        super(CalendarDateWidget, self).__init__(
            attrs={'class': 'datepicker', 'size': '10'}, format=format)

class CalendarTimeWidget(forms.TimeInput):
    format = getattr(settings, 'CALENDAR_TIME_FORMAT', '%H:%M')

    def __init__(self, attrs={}, format=None):
        super(CalendarTimeWidget, self).__init__(
            attrs={'class': 'timepicker', 'size': '10'}, format=format)


class CalendarSplitDateTimeWidget(forms.SplitDateTimeWidget):
    date_format = getattr(settings, 'CALENDAR_DATE_FORMAT', '%d.%m.%Y')
    time_format = getattr(settings, 'CALENDAR_TIME_FORMAT', '%H:%M')

    def __init__(self, attrs=None):
        widgets = [CalendarDateWidget, CalendarTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u"%s %s %s %s" % (u'Datum', 
            rendered_widgets[0], u'Čas', rendered_widgets[1]))
                