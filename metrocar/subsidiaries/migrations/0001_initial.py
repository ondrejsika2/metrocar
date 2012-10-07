# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subsidiary'
        db.create_table('subsidiaries_subsidiary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('house_number', self.gf('django.db.models.fields.IntegerField')(max_length=8)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('tax_rate', self.gf('django.db.models.fields.FloatField')(default=19)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('use_onboard_unit', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('subsidiaries', ['Subsidiary'])


    def backwards(self, orm):
        # Deleting model 'Subsidiary'
        db.delete_table('subsidiaries_subsidiary')


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'subsidiaries.subsidiary': {
            'Meta': {'object_name': 'Subsidiary'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'house_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'default': '19'}),
            'use_onboard_unit': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['subsidiaries']