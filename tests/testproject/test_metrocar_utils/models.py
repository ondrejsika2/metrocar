'''
Created on 23.4.2010

@author: xaralis
'''

from django.db import models

from metrocar.utils.models import SystemModel, CloneableModelMixin

class DummyModel(SystemModel, CloneableModelMixin):
    testfield = models.IntegerField()