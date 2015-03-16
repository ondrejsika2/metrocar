# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Migration(SchemaMigration):

    def forwards(self, orm):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

