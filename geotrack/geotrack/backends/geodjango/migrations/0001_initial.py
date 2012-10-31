# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LastKnownPosition'
        db.create_table('geodjango_lastknownposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('geodjango', ['LastKnownPosition'])


    def backwards(self, orm):
        # Deleting model 'LastKnownPosition'
        db.delete_table('geodjango_lastknownposition')


    models = {
        'geodjango.lastknownposition': {
            'Meta': {'object_name': 'LastKnownPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'unit_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['geodjango']