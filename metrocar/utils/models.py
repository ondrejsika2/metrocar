import copy
from decimal import Decimal
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site, SiteManager
from django.shortcuts import loader
from django.template.context import Context

class CloneableModelMixin:
    def clone(self, **kwargs):
        """
        Mixin method to add capability to clone model.
        The new clone has its params changed according to values in kwargs
        """
        if not self.pk:
            raise ValueError('Instance must be saved before it can be cloned.')
        
        duplicate = copy.copy(self)
        duplicate.pk = None
        duplicate.id = None
        
        # change according to kwargs
        for field in self._meta.fields:
            if field is not self._meta.pk and kwargs.has_key(field.name):
                setattr(duplicate, field.name, kwargs[field.name])
        duplicate.save()
        # ... but the trick loses all ManyToMany relations.
        for field in self._meta.many_to_many:
            source = getattr(self, field.attname)
            destination = getattr(duplicate, field.attname)
            for item in source.all():
                destination.add(item)
        return duplicate
    
class SystemModel(models.Model):
    deleteable = models.BooleanField(null=False, blank=False, default=True,
        verbose_name=_('Deleteable'))

    class Meta:
        abstract = True
        
    def delete(self):
        """
        Overload of delete to protect model from deletion if it is 'system'
        """
        if self.deleteable is True:
            super(SystemModel, self).delete()
        else:
            raise AssertionError('Object is marked as non deleteable')

class LogMessage(models.Model):
    level_no = models.IntegerField(_('Level number'), null=False)
    created = models.DateTimeField(_('Time'), null=False, default=datetime.now)
    message = models.TextField(_('Message'), null=False, default="")
    
    class Meta:
        verbose_name = _('Log message')
        verbose_name_plural = _('Log messages')

class SiteSettingsManager(models.Manager):
    def get_current(self):
        """
        Returns or creates current SiteSettings object.
        """
        site = Site.objects.get_current()
        s, created = self.get_or_create(site_ptr=site)
        return s

class SiteSettings(Site):
    gps_check_interval = models.IntegerField(blank=False, null=False,
        default=8000, verbose_name=_('GPS check interval'))
    gps_min_distance_location = models.DecimalField(decimal_places=2,
        max_digits=8, blank=False, null=False, default=Decimal("100"),
        verbose_name=_('GPS minimal distance location'))
    gps_min_time_location = models.DecimalField(decimal_places=2, max_digits=8,
        blank=False, null=False, default=Decimal("30000"),
        verbose_name=_('GPS minimal time location'))
    gps_location_send_interval = models.IntegerField(blank=False, null=False,
        default=900000, verbose_name=_('GPS location send interval'))
    gps_retry_send_interval = models.IntegerField(blank=False, null=False,
        default=180000, verbose_name=_('GPS retry send interval'))
    gps_echo_interval = models.IntegerField(blank=False, null=False,
        default=180000, verbose_name=_('GPS echo interval'))
    reservation_min_duration = models.IntegerField(blank=False, null=False,
        default=1300, verbose_name=_('Minimal duration of reservation'))
    reservation_max_duration = models.IntegerField(blank=False, null=False,
        default=2592000, verbose_name=_('Maximal duration of reservation'))
    reservation_use_storno_fees = models.BooleanField(blank=False, null=False,
        default=True, verbose_name=_('Use storno fees for reservations'))
    reservation_cancel_interval = models.IntegerField(blank=False, null=False,
        default=1200, verbose_name=_('Reservation cancel interval'))
    reservation_money_multiplier = models.DecimalField(decimal_places=2, 
        max_digits=4, blank=False, null=False, default=Decimal("1.5"), 
        verbose_name=_('Required money multiplier'), help_text=_('Multiplier '
        'applied when calculating required money for reservation.'))
    
    objects = SiteSettingsManager()
    
    class Meta:
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')
        
    def get_unit_settings_dict(self):
        """
        Returns dictionary with car comm information
        """
        return {
            'gps_check_interval': self.gps_check_interval,
            'gps_min_distance_location': self.gps_min_distance_location,
            'gps_min_time_location': self.gps_min_time_location,
            'gps_location_send_interval': self.gps_location_send_interval,
            'gps_retry_send_interval': self.gps_retry_send_interval,
            'gps_echo_interval': self.gps_echo_interval
        }
        
class EmailTemplate(models.Model):
    code = models.CharField(max_length=10, blank=False, null=False, unique=False,
        verbose_name=_('Code'))
    name = models.CharField(max_length=50, blank=False, null=False, unique=False,
        verbose_name=_('Name'))
    subject = models.CharField(max_length=100, blank=False, null=False,
        verbose_name=_('Subject'))
    content = models.TextField(blank=False, null=False,
        verbose_name=_('Content'))
    language = models.CharField(max_length=2, choices=settings.LANG_CHOICES, verbose_name=_('Language'))
    
    class Meta:
        verbose_name = _('E-mail template')
        verbose_name_plural = _('E-mail templates')
        unique_together = (('code', 'language'),)
        
    def _render_str(self, str, **kwargs):
        """
        Renders string with context made of kwargs using django rendering engine
        """
        template = loader.get_template_from_string(str)
        return template.render(Context(kwargs))
        
    def render_content(self, **kwargs):
        """
        Renders e-mail template content using django view rendering engine and returns
        string content

        kwargs may contain parameters which render method will try to substitude
        in content
        """
        return self._render_str(self.content, **kwargs)
    
    def render_subject(self, **kwargs):
        """
        Renders e-mail template subject using django view rendering engine and returns
        string content

        kwargs may contain parameters which render method will try to substitude
        in subject
        """
        return self._render_str(self.subject, **kwargs)
