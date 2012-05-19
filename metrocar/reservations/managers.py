'''
Created on 7.5.2010

@author: xaralis
'''
from datetime import datetime, timedelta

from django.contrib.gis.db import models
from django.db.transaction import commit_on_success

class ReservationManager(models.GeoManager):
    @commit_on_success
    def create_reservation(self, user, car, datetime_from, datetime_till, **kwargs):
        """
        Creates new reservation with all validation included.
        """
        from django.conf import settings

        reservation = self.model(user=user, car=car,
            reserved_from=datetime_from, reserved_until=datetime_till)

        val_res, val_errs = reservation.is_valid()
        if not val_res:
            return False

        # import plugins given in settings
        plugins = []
        for plugin in settings.RESERVATION_PLUGINS:
            plugin_name = plugin.split('.')[-1]
            plugin_module = '.'.join(plugin.split('.')[0:-1])
            module = __import__(plugin_module, globals(), locals(), [ plugin_name ])
            plugins.append(getattr(module, plugin_name))

        # pre-save plugins (handled in settings)
        for plugin in plugins:
            plugin.pre_save(reservation, **kwargs)

        reservation.save()

        # post-save plugins (handled in settings)
        for plugin in plugins:
            plugin.post_save(reservation, **kwargs)

        return reservation

    def to_be_finished(self):
        """
        Returns queryset with reservations which are to be finished by
        reservation deamon
        Those are reservation which:
          1. have been started
          2. have not been finished
          3. have no pending journey
          4. their reservation time has elapsed
        """
        qs = self.running().filter(reserved_until__lte=datetime.now())
        qs.exclude(journeys__end_datetime__isnull=False)
        return qs

    def running(self):
        """
        Returns queryset with reservations which are running right now
        """
        return self.pending().filter(started__isnull=False, ended__isnull=True)

    def pending(self):
        """
        Returns only reservations which are waiting to start
        """
        return self.get_query_set().filter(finished=False)

    def waiting_to_start(self):
        """
        Returns only reservations which have not started yet
        """
        return self.get_query_set().filter(started__isnull=True)

    def finished(self):
        """
        Returns only reservations which have been finished
        """
        return self.get_query_set().filter(finished=True)

    def non_finished(self):
        """
        Returns only reservations which have not been finished
        """
        return self.get_query_set().filter(finished=False)

    def to_cancel(self):
        """
        Returns all reservation which are subject to cancel
        """
        from metrocar.utils.models import SiteSettings
        cancel_interval = SiteSettings.objects.get_current().reservation_cancel_interval
        datetime_limit = datetime.now() - timedelta(seconds=cancel_interval)
        return self.get_query_set().filter(reserved_from__lte=datetime_limit)

    def without_journey(self):
        """
        Returns all reservations without set journey information
        """
        return self.get_query_set().filter(path__isnull=True, reserved_until__lte=datetime.now())

class ReservationReminderManager(models.Manager):
    def create_for_reservation(self, reservation, datetime):
        """
        Creates new reminder on datetime for reservation.
        """
        from django.conf import settings
        target_datetime = reservation.reserved_from \
            - timedelta(seconds=settings.RESERVATION_REMINDER_CRON_INTERVAL)

        if datetime > target_datetime:
            raise ValueError(_('Datetime is to late to create a reminder for '
                'reservation. Maximum datetime is %s.') % target_datetime)

        reminder = self.model(datetime=datetime,
            reservation=reservation)
        return reminder

    def pending(self):
        """
        Returns all pending reminders.
        """
        return self.get_query_set().filter(sent=False,
            reservation__datetime_from__gte=datetime.now(),
            reservation__cancelled=False)

    def ready_to_send(self):
        """
        Returns reminders which are ready to be send on current deamon run.
        """
        from django.conf import settings
        now = datetime.now()
        target_datetime = now + timedelta(seconds=settings.RESERVATION_REMINDER_CRON_INTERVAL)
        return self.pending().filter(datetime__gte=now, datetime__lt=target_datetime)

class ReservationBillManager(models.Manager):
    def create_for_reservation(self, reservation):
        """
        Generates bill for a reservation and saves it.
        """
        bill = self.model(
            reservation=reservation,
            money_amount=-reservation.price,
            account=reservation.user.account
        )
        bill.save()
        return bill

