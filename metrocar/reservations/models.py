#RESERVATION

from datetime import datetime, timedelta

from django.db.models.signals import post_save, pre_delete
from django.db.transaction import commit_on_success
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiLineString
from django.utils.translation import ugettext_lazy as _

from metrocar.user_management.models import MetrocarUser, AccountActivity
from metrocar.utils.models import SiteSettings
from django.utils.encoding import force_unicode

import managers

class ReservationError(Exception):
    pass

class Reservation(models.Model):
    cancelled = models.BooleanField(blank=False, null=False, default=False,
        verbose_name=_('Cancelled'))
    comment = models.TextField(blank=True, null=False, default='',
        verbose_name=_('Comment'))
    created = models.DateTimeField(blank=False, null=False, editable=False,
        verbose_name=_('Created'))
    ended = models.DateTimeField(blank=True, null=True, verbose_name=_('Ended'))
    finished = models.BooleanField(blank=False, null=False, editable=False,
        default=False, verbose_name=_('Finished'))
    is_service = models.BooleanField(blank=False, null=False, default=False,
        verbose_name=_('Is service'))
    modified = models.DateTimeField(blank=False, null=False, editable=False,
        verbose_name=_('Modified'))
    price = models.DecimalField(decimal_places=3, max_digits=8, blank=False,
        null=False, editable=False, default=0,verbose_name=_('Price'))
    reserved_from = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Reserved from'))
    reserved_until = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Reserved until'))
    started = models.DateTimeField(blank=True, null=True,
        verbose_name=_('Started'))
    path = models.MultiLineStringField(null=True, blank=True,
        default=None, spatial_index=False, verbose_name=_('Path'))
    
    user = models.ForeignKey(MetrocarUser, verbose_name=_('User'),
        related_name='reservations')
    car = models.ForeignKey('cars.Car', verbose_name=_('Car'),
        related_name='reservations')
    
    objects = managers.ReservationManager()

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')

    def __unicode__(self):
        return "%s - %s" % (datetime.strftime(self.reserved_from, 
            '%H:%M:%S %A, %d.%m.%Y'), datetime.strftime(self.reserved_until, 
            '%H:%M:%S %A, %d.%m.%Y'))
    
    def save(self, *args, **kwargs):
        """
        Overload save method for settings created and modified params.
        """
        now = datetime.now()
        if not self.pk:
            self.created = now
        self.modified = now
        super(Reservation, self).save(*args, **kwargs)
    
    def is_valid(self):
        """
        Proxy to validate method
        """
        return Reservation.validate(self.user, self.car, self.reserved_from,
            self.reserved_until)
    
    @classmethod
    def validate(cls, user, car, datetime_from, datetime_till):
        """
        Test if reservation can be created by using submitted data
        
        Test following things:
            - datetime_from preceeds datetime_till
            - datetime_from is not in the past
            - min/max reservation duration limit does not take place
            - valid pricelist exists
            - account balance is sufficent
            - no conflicting reservation exists 
        """
        from metrocar.cars.models import Car

        assert isinstance(user, MetrocarUser)
        assert isinstance(car, Car)
        assert isinstance(datetime_from, datetime)
        assert isinstance(datetime_till, datetime)

        site_settings = SiteSettings.objects.get_current()
        errors = []

        # datetime checks
        if datetime_from > datetime_till:
            errors.append(force_unicode(_('From datetime must be before till.')))
        now = datetime.now()
        if now >= datetime_from:
            errors.append(force_unicode(_('Cannot create reservation in the past.')))
        duration = int(datetime_till.strftime('%s')) - int(datetime_from.strftime('%s'))
        if duration < site_settings.reservation_min_duration:
            errors.append(force_unicode(_('Minimum duration of %s minutes not reached.'))
                % str(round(site_settings.reservation_min_duration / 60)))
        if duration > site_settings.reservation_max_duration:
            errors.append(force_unicode(_('Maximum duration of %s has been exceeded.'))
                % str(round(site_settings.reservation_max_duration / 86400)))
        if car.model.get_pricelist() == False:
            errors.append(force_unicode(_('No valid pricelist for selected car model.')))

        # user account checks
        price_estimation = cls.get_price_estimation(car, datetime_from,
            datetime_till)
        required_money_amount = price_estimation * \
            site_settings.reservation_money_multiplier

        if user.account.balance < required_money_amount:
            errors.append(force_unicode(_('You don\'t have enough money '
                'to create reservation. Required account balance is %d.'))
                % required_money_amount)

        # conflicts check
        conflicts = cls.find_conflicts(car, datetime_from, datetime_till)

        # check for conflicts with other reservations
        if len(conflicts) != 0:
            errors.append(force_unicode(_('Reservation cannot be created due '
                'to conflicting time')))

        if len(errors) == 0:
            return True, []
        else:
            return False, errors
    
    def ready_to_finish(self):
        """
        Returns true if reservation is ready to be finished
        """
        from metrocar.cars.models import Parking
        if self.finished or self.ended is not None: return True
        if self.started is None: return False
        
        if not self.car.dedicated_parking_only:
            # cars which doesn't have dedicated parking are little trouble
            # as we can't rightfully decide if their reservation can be 
            # finished
            # => they are collected by reservation deamon
            return False
        else:
            parking = Parking.objects.filter(
                polygon__contains=self.car.last_position)
            if len(parking) != 0:
                return True
            return False
        
    def is_in_conflict(self):
        """
        Returns true if reservation has some conflicts with other reservations.
        """
        return len(self.get_conflicts()) != 0
    
    def get_conflicts(self):
        """
        Returns all Reservation object which are conflicting with current
        reservation
        """
        conflicts = self.find_conflicts(self.car, self.reserved_from, 
            self.reserved_until)
        if self.pk:
            conflicts.exclude(pk=self.pk)
        return conflicts
    
    @classmethod
    def find_conflicts(cls, car, dt_from, dt_till):
        """
        Returns queryset of all Reservation objects which are conflicting  
        for given datetime intervals and car
        """
        from django.db.models import Q
        conflicts = Reservation.objects.filter(
            Q(car=car),
            Q(cancelled=False),
            Q(reserved_from__lte=dt_from, reserved_until__gte=dt_from) |
            Q(reserved_from__lte=dt_till, reserved_until__gte=dt_till)
        )
        return conflicts
    
    def is_running(self):
        """
        Returns true if reservation is currently running
        """
        return self.reserved_from <= datetime.now() and not self.finished
        
    def cancel(self):
        """
        Cancels reservation and creates proper StornoFee object.
        """
        if not self.is_running():
            from metrocar.tarification.models import StornoFee
            from metrocar.utils.models import SiteSettings
            if SiteSettings.objects.get_current().reservation_use_storno_fees:
                fee = StornoFee.objects.create_for_reservation(self)
                self.price = fee.money_amount
            self.cancelled = True
            self.finished = True
            self.save()
        else:
            raise ReservationError(_('Cannot cancel reservation which already begun'))
    
    @classmethod
    def refresh_journey_data(cls, sender, **kwargs):
        """
        Refreshes path information from journeys
        """
        reservation = kwargs['instance'].reservation
        if reservation is None: return
        
        # refresh path
        if len(reservation.journeys.all()) == 0: return
        line_strings = []
        for j in reservation.journeys.order_by('pk'):
            if j.path is not None:
                for ls in j.path:
                    line_strings.append(ls)
        if len(line_strings) != 0:
            reservation.path = MultiLineString(*line_strings)
        else:
            reservation.path = None
        reservation.save()
    
    def get_pricelist(self):
        """
        Returns the pricelist, which is used for the reservation
        """
        from metrocar.tarification.models import Pricelist
        try:
            if self.finished:
                return Pricelist.objects.filter(model=self.car.model,
                    valid_from__lte=self.created).order_by('valid_from')[0]
            else:
                return Pricelist.objects.valid().filter(model=self.car.model,
                    valid_from__lte=self.created).order_by('valid_from')[0]
        except IndexError:
            raise ReservationError('No valid pricelist found for date %s' 
                % self.created)
    
    def get_pricing_summary(self):
        """
        Returns reservation pricing summary for template viewing purposes.
        """
        if not self.finished:
            return None
        pricing = []
        total_price, km_price, time_price = (0, 0, 0)
        for j in self.journeys.all().order_by('pk'):
            pi = j.get_pricing_info()
            total_price += pi['total_price']
            km_price += pi['km_price']
            time_price += pi['time_price']
            pricing.append(pi)
        return {
            'km_price': km_price,
            'time_price': time_price,
            'total_price': total_price,
            'parts': pricing
        }
    
    def get_total_price(self):
        """
        Returns total price for reservation
        """
        if not self.finished:
            return 0
        total_price = 0
        for j in self.journeys.all(): total_price += j.total_price
        return total_price
    
    def estimate_price(self):
        """
        Proxy to get_price_estimation class method
        """
        return Reservation.get_price_estimation(self.car, self.reserved_from,
            self.reserved_until)
    
    @classmethod
    def get_price_estimation(cls, car, dt_from, dt_till):
        """
        Returns estimation based mainly on time of reservation
        """
        from decimal import Decimal
        pricelist = car.model.get_pricelist()
        if pricelist:
            duration = Decimal(int(dt_till.strftime('%s')) - int(dt_from.strftime('%s'))) / Decimal(3600)
            # try to estimate time and kms, expect ~ 10km per hour
            return (pricelist.price_per_hour + pricelist.price_per_km * 10) * duration
        else:
            raise ReservationError('No suitable pricelist found.')
    
    def finish(self, finish_datetime=datetime.now(), by_daemon=False):
        """
        Marks reservation as finished, starts normalization of Journeys
        and finally creates ReservationBill for current reservation.
        """
        from metrocar.cars.models import Journey
        if self.finished: return True
        if self.ready_to_finish() or by_daemon:
            # normalize journey objects (splitting, filling up etc.)
            Journey.objects.normalize_for_reservation(self)
            
            self.finished = True
            self.ended = finish_datetime
            self.price = self.get_total_price()
            self.save()
            
            # create bill for that reservation
            ReservationBill.objects.create_for_reservation(self)
            return True
        return False  

class ReservationReminder(models.Model):
    datetime = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Date time'))
    sent = models.BooleanField(blank=False, null=False, editable=False,
        default=False, verbose_name=_('Sent'))
    
    reservation = models.OneToOneField(Reservation, verbose_name=_('Reservation'))

    objects = managers.ReservationReminderManager()

    class Meta:
        verbose_name = _('Reservation reminder')
        verbose_name_plural = _('Reservation reminders')

    def __unicode__(self):
        return self.reservation.__unicode__()
    
    def send(self):
        """
        Sends reminder by e-mail service.
        """
        EmailSender.send_mail( [ self.reservation.user.email ], 'RES_REM', self.reservation.user.language, self.reservation )

        self.sent = True
        self.save()
    
class ReservationBill(AccountActivity):
    reservation = models.ForeignKey(Reservation, verbose_name=_('Reservation'))
    
    objects = managers.ReservationBillManager()
    
    class Meta:
        verbose_name = _('Reservation bill')
        verbose_name_plural = _('Reservation bills')
        
    def __unicode__(self):
        return _('Bill for reservation %s') % self.reservation
