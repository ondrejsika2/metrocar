"""
These models are draft only. Most work is not done and changes in model schema
is to be expected during future development.
"""

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from metrocar.user_management.models import MetrocarUser, AccountActivity


class FixedPaymentTariff(models.Model):
    """
    Represents user tariff which allows users to drive for less if they use
    carsharing services often.

    It consists of several benefits:
      - free kms for month
      - correction ratio for regular price which lowers the regular prices
    """
    description = models.TextField(blank=False, null=False,
        verbose_name=_('Description'))
    free_km_per_month = models.DecimalField(decimal_places=3, max_digits=8,
        blank=False, null=False, default=0, verbose_name=_('Free km per month'))
    name = models.CharField(max_length=80, blank=False, null=False,
        verbose_name=_('Name'))
    price_correction_ratio = models.DecimalField(decimal_places=3, max_digits=8,
        blank=False, null=False, default=0, verbose_name=_('Price correction ratio'))
    price_per_month = models.DecimalField(decimal_places=3, max_digits=8,
        blank=False, null=False, default=0, verbose_name=_('Price per month'))
    valid_from = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Valid from'))
    valid_until = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Valid until'))
    visible = models.BooleanField(blank=False, null=False, default=False,
        verbose_name=_('Visible'))

    class Meta:
        verbose_name = _('Fixed payment tariff')
        verbose_name_plural = _('Fixed payment tariffs')

    def __unicode__(self):
        return self.name

class FixedPaymentTariffBill(AccountActivity):
    tariff = models.ForeignKey(FixedPaymentTariff,
        verbose_name=_('Fixed payment tariff'))
    user = models.ForeignKey(MetrocarUser, verbose_name=_('User'))
    day_count = models.PositiveSmallIntegerField(max_length=2, blank=False,
        null=False, default=30, verbose_name=_('Day count'))

class FixedPaymentTariffUserDetails(models.Model):
    accumulated_free_km = models.DecimalField(decimal_places=3, max_digits=8,
        blank=False, null=False, default=0, verbose_name=_('Accumulated free km'))
    tariff = models.ForeignKey(FixedPaymentTariff, verbose_name=_('Fixed payment tariff'))
    user = models.ForeignKey(MetrocarUser, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Fixed payment tariff user details')
        verbose_name_plural = _('Fixed payment tariff user details')

    def __unicode__(self):
        return _('%s tariff details') % self.user

    #TODO overload delete to make bills

    def transfer_to_next_month(self):
        #TODO bill generation
        pass

class FixedPaymentTariffHistory(models.Model):
    date_from = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Date from'))
    date_until = models.DateTimeField(blank=False, null=False,
        verbose_name=_('Date until'))
    tariff = models.OneToOneField(FixedPaymentTariff, verbose_name=_('Tariff'))
    user = models.OneToOneField(MetrocarUser, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Fixed payment tariff history')
        verbose_name_plural = _('Fixed payment tariff history')

    def __unicode__(self):
        return self.user.__unicode__()

class FreeKmUsageHistoryManager(models.Manager):
    @classmethod
    def create_for_reservation(cls, reservation):
        """
        Returns free km usage history for a reservation.
        """
        return FreeKmUsageHistory()

class FreeKmUsageHistory(models.Model):
    amount = models.DecimalField(decimal_places=3, max_digits=8, blank=False,
        null=False, verbose_name=_('Km amount'))
    datetime = models.DateTimeField(blank=False, null=False,
        default=datetime.now(), verbose_name=_('Datetime'))
    user = models.OneToOneField(MetrocarUser, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Free Km usage history')
        verbose_name_plural = _('Free Km usage history')

    def __unicode__(self):
        return _('Free km usage history for %s') % self.user

