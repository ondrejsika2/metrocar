'''
Created on 11.3.2010

@author: xaralis
'''

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.models import FlatPage

class Meta(models.Model):
    flatpage = models.OneToOneField(FlatPage, verbose_name=_('Flatpage'))
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Keywords'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    active = models.BooleanField(blank=False, null=False, default=True, verbose_name=_('Active'))
    date_created = models.DateTimeField(verbose_name=_('Created'), editable=False, null=False)
    date_modified = models.DateTimeField(verbose_name=_('Modified'), editable=False, null=False)
    
    class Meta:
        verbose_name = _('Meta information')
        verbose_name_plural = _('Meta informations')
    
    def __unicode__(self):
        return self.flatpage.title
    
    def save(self):
        if not self.pk:
            self.date_created = datetime.now()
            self.date_modified = datetime.now()
        super(Meta, self).save()
        