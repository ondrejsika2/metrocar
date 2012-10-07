# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LogMessage'
        db.create_table('utils_logmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level_no', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('message', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('utils', ['LogMessage'])

        # Adding model 'SiteSettings'
        db.create_table('utils_sitesettings', (
            ('site_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True, primary_key=True)),
            ('gps_check_interval', self.gf('django.db.models.fields.IntegerField')(default=8000)),
            ('gps_min_distance_location', self.gf('django.db.models.fields.DecimalField')(default='100', max_digits=8, decimal_places=2)),
            ('gps_min_time_location', self.gf('django.db.models.fields.DecimalField')(default='30000', max_digits=8, decimal_places=2)),
            ('gps_location_send_interval', self.gf('django.db.models.fields.IntegerField')(default=900000)),
            ('gps_retry_send_interval', self.gf('django.db.models.fields.IntegerField')(default=180000)),
            ('gps_echo_interval', self.gf('django.db.models.fields.IntegerField')(default=180000)),
            ('reservation_min_duration', self.gf('django.db.models.fields.IntegerField')(default=1300)),
            ('reservation_max_duration', self.gf('django.db.models.fields.IntegerField')(default=2592000)),
            ('reservation_use_storno_fees', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('reservation_cancel_interval', self.gf('django.db.models.fields.IntegerField')(default=1200)),
            ('reservation_money_multiplier', self.gf('django.db.models.fields.DecimalField')(default='1.5', max_digits=4, decimal_places=2)),
        ))
        db.send_create_signal('utils', ['SiteSettings'])

        # Adding model 'EmailTemplate'
        db.create_table('utils_emailtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('utils', ['EmailTemplate'])

        # Adding unique constraint on 'EmailTemplate', fields ['code', 'language']
        db.create_unique('utils_emailtemplate', ['code', 'language'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailTemplate', fields ['code', 'language']
        db.delete_unique('utils_emailtemplate', ['code', 'language'])

        # Deleting model 'LogMessage'
        db.delete_table('utils_logmessage')

        # Deleting model 'SiteSettings'
        db.delete_table('utils_sitesettings')

        # Deleting model 'EmailTemplate'
        db.delete_table('utils_emailtemplate')


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'utils.emailtemplate': {
            'Meta': {'unique_together': "(('code', 'language'),)", 'object_name': 'EmailTemplate'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'utils.logmessage': {
            'Meta': {'object_name': 'LogMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_no': ('django.db.models.fields.IntegerField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'utils.sitesettings': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'SiteSettings', '_ormbases': ['sites.Site']},
            'gps_check_interval': ('django.db.models.fields.IntegerField', [], {'default': '8000'}),
            'gps_echo_interval': ('django.db.models.fields.IntegerField', [], {'default': '180000'}),
            'gps_location_send_interval': ('django.db.models.fields.IntegerField', [], {'default': '900000'}),
            'gps_min_distance_location': ('django.db.models.fields.DecimalField', [], {'default': "'100'", 'max_digits': '8', 'decimal_places': '2'}),
            'gps_min_time_location': ('django.db.models.fields.DecimalField', [], {'default': "'30000'", 'max_digits': '8', 'decimal_places': '2'}),
            'gps_retry_send_interval': ('django.db.models.fields.IntegerField', [], {'default': '180000'}),
            'reservation_cancel_interval': ('django.db.models.fields.IntegerField', [], {'default': '1200'}),
            'reservation_max_duration': ('django.db.models.fields.IntegerField', [], {'default': '2592000'}),
            'reservation_min_duration': ('django.db.models.fields.IntegerField', [], {'default': '1300'}),
            'reservation_money_multiplier': ('django.db.models.fields.DecimalField', [], {'default': "'1.5'", 'max_digits': '4', 'decimal_places': '2'}),
            'reservation_use_storno_fees': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['utils']