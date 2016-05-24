# encoding: utf-8
import math
from types import NoneType
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from pipetools import maybe, X, xcurry

from django.conf import settings
from django.contrib.gis.geos import MultiLineString
from django.db import models
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _, ngettext
from rest_framework.exceptions import APIException
from django.db.models import get_model

from metrocar.reservations.business import managers
from metrocar.user_management.models import MetrocarUser, AccountActivity, Account
from metrocar.utils.exceptions import CustomAPIException
from metrocar.utils.models import SiteSettings
from metrocar.utils.geo import get_car_last_position, create_journeys


RESERVATION_TIME_SHIFT = settings.RESERVATION_TIME_SHIFT


class ReservationError(Exception):
    pass

class Reservation(models.Model):
    cancelled = models.BooleanField(_('Cancelled'), default=False)
    comment = models.TextField(_('Comment'), blank=True, default='')
    ended = models.DateTimeField(_('Ended'), blank=True, null=True)
    finished = models.BooleanField(_('Finished'), default=False)
    is_service = models.BooleanField(_('Is service'), default=False)
    price = models.DecimalField(_('Price'), decimal_places=3, max_digits=8,
        default=0)
    reserved_from = models.DateTimeField(_('Reserved from'))
    reserved_until = models.DateTimeField(_('Reserved until'))
    started = models.DateTimeField(_('Started'), blank=True, null=True)
    user = models.ForeignKey(MetrocarUser, verbose_name=_('User'),
        related_name='reservations')
    car = models.ForeignKey('cars.Car', verbose_name=_('Car'),
        related_name='reservations')

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    objects = managers.ReservationManager()

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')

    def __unicode__(self):
        return unicode("%s - %s" % (datetime.strftime(self.reserved_from,
            '%H:%M:%S %A, %d.%m.%Y'), datetime.strftime(self.reserved_until,
            '%H:%M:%S %A, %d.%m.%Y')))

    def save(self, *args, **kwargs):

        if 'force_save_user' in kwargs:
            del kwargs['force_save_user']
        else:
            errors = Reservation.validate(self.user, self.car, self.reserved_from, self.reserved_until)
            if not errors[0] and len(errors[1]):
                raise CustomAPIException(errors[1])

        super(Reservation, self).save(*args, **kwargs)

    def is_valid(self):
        """
        Proxy to validate method
        """
        return Reservation.validate(self.user, self.car, self.reserved_from, self.reserved_until)

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
            - user has entered invoice address
        """
        site_settings = SiteSettings.objects.get_current()
        errors = []

        datetime_from = timezone.make_aware(datetime_from, timezone.now().tzinfo)
        datetime_till = timezone.make_aware(datetime_till, timezone.now().tzinfo)

        # datetime checks
        if datetime_from > datetime_till:
            errors.append(force_unicode(_('From datetime must be before till.')))
        now = datetime.utcnow()
        # lze udelat rezervaci nazpet v case o 1x RESERVATION_TIME_SHIFT
        if (now - timedelta(minutes=RESERVATION_TIME_SHIFT)) >= datetime_from:
            errors.append(force_unicode(_('Cannot create reservation in the past.')))
        duration = int(datetime_till.strftime('%s')) - int(datetime_from.strftime('%s'))
        if duration < site_settings.reservation_min_duration:
            errors.append(force_unicode(_('Minimum duration of %s minutes not reached.'))
                % str(round(site_settings.reservation_min_duration / 60)))
        if duration > site_settings.reservation_max_duration:
            if (site_settings.reservation_max_duration / 86400) >= 1:
                max_duration = round(site_settings.reservation_max_duration / 86400)
                err_msg = ngettext(
                    'Maximum duration of %(max_duration)s day has been exceeded.',
                    'Maximum duration of %(max_duration)s days has been exceeded.',
                    max_duration
                ) % {'max_duration' : max_duration}
            else:
                if (site_settings.reservation_max_duration / 3600) >= 1:
                    max_duration = round(site_settings.reservation_max_duration / 3600)
                    err_msg = ngettext(
                        'Maximum duration of %(max_duration)s hour has been exceeded.',
                        'Maximum duration of %(max_duration)s hours has been exceeded.',
                        max_duration
                    ) % {'max_duration' : max_duration}
                else:
                    max_duration = round(site_settings.reservation_max_duration / 60)
                    err_msg = ngettext(
                        'Maximum duration of %(max_duration)s minute has been exceeded.',
                        'Maximum duration of %(max_duration)s minutes has been exceeded.',
                        max_duration
                    ) % {'max_duration' : max_duration}
            errors.append(force_unicode(err_msg))
        if car.model.get_pricelist() == False:
            errors.append(force_unicode(_('No valid pricelist for selected car model.')))


        if not errors:
            # user account checks
            # if there already were some errors this might break
            price_estimation = cls.get_price_estimation(car, datetime_from,
                datetime_till)
            required_money_amount = price_estimation * \
                site_settings.reservation_money_multiplier

            if user.account.balance < required_money_amount:
                errors.append(force_unicode(_('You don\'t have enough money to create reservation. Required account balance is %s.'))
                    % ('%d %s' % (Decimal(required_money_amount), u'Kč')))

            #now check if user has entered invoice address
            #withouit address it would be impossible to create valid invoice
            if user.get_invoice_address() == None:
                errors.append(force_unicode(_('You need to enter your address first at yout account settings. We need this information for creation of invoice.')))



        # conflicts check
        conflicts = cls.find_conflicts(car, datetime_from, datetime_till)

        # check for conflicts with other reservations
        if len(conflicts) != 0:
            errors.append(force_unicode(_('Reservation cannot be created due to conflicting time')))

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
        elif settings.GEO_ENABLED:
            # is there a Parking that contains car's last_position?
            return (self.car > maybe
                | get_car_last_position
                | X['location']
                | 'POINT ({0} {1})'
                | xcurry(Parking.objects.filter, polygon__contains=X)
                | X.exists())

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
        if conflicts is not NoneType and conflicts.__len__() is 1:
            return []
        return conflicts


    def is_running(self):
        """
        Returns true if reservation is currently running
        """
        return self.reserved_from <= timezone.now() and not self.finished

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
        reservation = None
        try:
            reservation = kwargs['instance'].reservation
        except Exception:
            pass
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
            raise ReservationError(_('No valid pricelist found.'))

    def get_pricing_summary(self):
        """
        Returns reservation pricing summary for template viewing purposes.
        """
        if not self.finished:
            return None
        pricing = []
        total_price, km_price, time_price = (0, 0, 0)
        journeys = self.journeys.all().order_by('pk')
        for j in journeys:
            pi = j.get_pricing_info()
            if pi == None:
                continue
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

    def count_total_price(self):
        total_price = 0
        for j in self.journeys.all(): total_price += j.total_price

        pricelist = self.car.model.get_pricelist()
        total_price += (pricelist.pickup_fee + pricelist.reservation_fee)

        return total_price

    def count_total_price(self, journey):
        total_price = 0

        # get car's pricelist
        pricelist = self.car.model.get_pricelist()

        # add one-time fees
        total_price += (pricelist.pickup_fee + pricelist.reservation_fee)

        # add time based fee -> for every started hour
        total_price += Decimal(math.ceil(journey.duration/60)*float(pricelist.price_per_hour))

        # add distance based fee -> for kilometers (no rounding)
        total_price += Decimal((journey.length/1000)*float(pricelist.price_per_km))

        return total_price


    def get_total_price(self):
        """
        Returns total price for reservation
        """
        if not self.finished:
            return 0

        return self.count_total_price()

    def estimate_price(self, distance = 0):
        """
        Proxy to get_price_estimation class method
        """
        return Reservation.get_price_estimation(self.car, self.reserved_from,
            self.reserved_until, distance)

    @classmethod
    def get_price_estimation(cls, car, dt_from, dt_till, distance = 0):
        """
        Returns estimation based mainly on time of reservation
        """
        from decimal import Decimal
        pricelist = car.model.get_pricelist()
        if pricelist:
            # try to estimate time and kms
            price_data = pricelist.count_base_journey_price(dt_from, dt_till, distance)
            return (price_data['total_price'] + pricelist.pickup_fee + pricelist.reservation_fee)
        else:
            raise ReservationError('No suitable pricelist found.')

    @classmethod
    def get_price_by_distance(cls, car, distance):
        pricelist = car.model.get_pricelist()
        if pricelist:
            return pricelist.price_per_km * Decimal(distance)
        else:
            raise ReservationError('No suitable pricelist found.')

    @classmethod
    def get_base_price(cls, car, dt_from, dt_till):
        """
        Returns base price without estimation based mainly on time of reservation
        """
        from decimal import Decimal
        pricelist = car.model.get_pricelist()
        if pricelist:
            price_data = pricelist.count_base_journey_price(dt_from, dt_till, 0)
            return price_data['total_price']
        else:
            raise ReservationError('No suitable pricelist found.')

    def finish(self, finish_datetime=timezone.now(), by_daemon=False, normalize_journeys=True):
        """
        Marks reservation as finished, starts normalization of Journeys
        and finally creates ReservationBill for current reservation.
        """
        from metrocar.cars.models import Journey
        if self.finished: return True
        if self.ready_to_finish() or by_daemon:

            if not self.has_journey() and settings.GEO_ENABLED:
                # create Journeys from Geotrack log entries
                create_journeys(
                    start=self.started,
                    end=finish_datetime,
                    car=self.car,
                    user=self.user,
                    reservation=self)

            # normalize journey objects (splitting, filling up etc.)
            if normalize_journeys:
                Journey.objects.normalize_for_reservation(self)

            self.finished = True
            self.ended = finish_datetime
            self.price = self.get_total_price() # deduct money from user account
            self.save()
            # create bill for that reservation
            ReservationBill.objects.create_for_reservation(self)
            return True
        return False

    def has_journey(self):
        from metrocar.cars.models import Journey
        journeys = Journey.objects.filter(reservation=self)
        return len(journeys) > 0

    @property
    def datafile(self):

        # import models here to avoid circular reference
        from metrocar.cars.models import Journey
        from metrocar.car_unit_api.models import JourneyDataFile
        from django.core.exceptions import ObjectDoesNotExist

        # find journey
        journeys = Journey.objects.filter(reservation = self.id)
        if len(journeys) == 0:
            return None
        else:
            journey = journeys[0]

        print "Reservation id: ", self.id
        print "Journey id: ", journey.id

        # find datafile
        try:
            datafile = JourneyDataFile.objects.get(journey = journey.id)
        except ObjectDoesNotExist:
            datafile = None

        if datafile == None:
            print "No file"
            return None
        else:
            print "File id: ", datafile.id
            return datafile.id

class ReservationReminder(models.Model):
    datetime = models.DateTimeField(_('Date time'))
    sent = models.BooleanField(_('Sent'), editable=False, default=False)

    reservation = models.OneToOneField(Reservation, verbose_name=_('Reservation'))

    objects = managers.ReservationReminderManager()

    class Meta:
        verbose_name = _('Reservation reminder')
        verbose_name_plural = _('Reservation reminders')

    def __unicode__(self):
        return self.reservation.__unicode__()

    def send(self):
        """
        Sends reminnder by e-mail service.
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
