# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FixedPaymentTariff'
        db.create_table('tariffs_fixedpaymenttariff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('free_km_per_month', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('price_correction_ratio', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('price_per_month', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')()),
            ('valid_until', self.gf('django.db.models.fields.DateTimeField')()),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tariffs', ['FixedPaymentTariff'])

        # Adding model 'FixedPaymentTariffBill'
        db.create_table('tariffs_fixedpaymenttariffbill', (
            ('accountactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.AccountActivity'], unique=True, primary_key=True)),
            ('tariff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tariffs.FixedPaymentTariff'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_management.MetrocarUser'])),
            ('day_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30, max_length=2)),
        ))
        db.send_create_signal('tariffs', ['FixedPaymentTariffBill'])

        # Adding model 'FixedPaymentTariffUserDetails'
        db.create_table('tariffs_fixedpaymenttariffuserdetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accumulated_free_km', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('tariff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tariffs.FixedPaymentTariff'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_management.MetrocarUser'])),
        ))
        db.send_create_signal('tariffs', ['FixedPaymentTariffUserDetails'])

        # Adding model 'FixedPaymentTariffHistory'
        db.create_table('tariffs_fixedpaymenttariffhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_from', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_until', self.gf('django.db.models.fields.DateTimeField')()),
            ('tariff', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tariffs.FixedPaymentTariff'], unique=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.MetrocarUser'], unique=True)),
        ))
        db.send_create_signal('tariffs', ['FixedPaymentTariffHistory'])

        # Adding model 'FreeKmUsageHistory'
        db.create_table('tariffs_freekmusagehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 7, 0, 0))),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.MetrocarUser'], unique=True)),
        ))
        db.send_create_signal('tariffs', ['FreeKmUsageHistory'])


    def backwards(self, orm):
        # Deleting model 'FixedPaymentTariff'
        db.delete_table('tariffs_fixedpaymenttariff')

        # Deleting model 'FixedPaymentTariffBill'
        db.delete_table('tariffs_fixedpaymenttariffbill')

        # Deleting model 'FixedPaymentTariffUserDetails'
        db.delete_table('tariffs_fixedpaymenttariffuserdetails')

        # Deleting model 'FixedPaymentTariffHistory'
        db.delete_table('tariffs_fixedpaymenttariffhistory')

        # Deleting model 'FreeKmUsageHistory'
        db.delete_table('tariffs_freekmusagehistory')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        },
        'tariffs.fixedpaymenttariff': {
            'Meta': {'object_name': 'FixedPaymentTariff'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'free_km_per_month': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'price_correction_ratio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'price_per_month': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tariffs.fixedpaymenttariffbill': {
            'Meta': {'object_name': 'FixedPaymentTariffBill', '_ormbases': ['user_management.AccountActivity']},
            'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'}),
            'day_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30', 'max_length': '2'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tariffs.FixedPaymentTariff']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_management.MetrocarUser']"})
        },
        'tariffs.fixedpaymenttariffhistory': {
            'Meta': {'object_name': 'FixedPaymentTariffHistory'},
            'date_from': ('django.db.models.fields.DateTimeField', [], {}),
            'date_until': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tariff': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tariffs.FixedPaymentTariff']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.MetrocarUser']", 'unique': 'True'})
        },
        'tariffs.fixedpaymenttariffuserdetails': {
            'Meta': {'object_name': 'FixedPaymentTariffUserDetails'},
            'accumulated_free_km': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tariffs.FixedPaymentTariff']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_management.MetrocarUser']"})
        },
        'tariffs.freekmusagehistory': {
            'Meta': {'object_name': 'FreeKmUsageHistory'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.MetrocarUser']", 'unique': 'True'})
        },
        'user_management.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'account'", 'unique': 'True', 'to': "orm['user_management.MetrocarUser']"})
        },
        'user_management.accountactivity': {
            'Meta': {'object_name': 'AccountActivity'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': "orm['user_management.Account']"}),
            'account_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '8', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'credited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'user_management.company': {
            'Meta': {'object_name': 'Company'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'dic': ('metrocar.utils.fields.DicField', [], {'max_length': '12', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'ic': ('metrocar.utils.fields.IcField', [], {'max_length': '8', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_registry_number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'user_management.metrocaruser': {
            'Meta': {'object_name': 'MetrocarUser', '_ormbases': ['auth.User']},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_management.Company']", 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'drivers_licence_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'home_subsidiary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subsidiaries.Subsidiary']"}),
            'identity_card_number': ('metrocar.utils.fields.IdentityCardNumberField', [], {'max_length': '9'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'primary_phone': ('metrocar.utils.fields.PhoneField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'secondary_phone': ('metrocar.utils.fields.PhoneField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'variable_symbol': ('django.db.models.fields.IntegerField', [], {'max_length': '12', 'null': 'True'})
        }
    }

    complete_apps = ['tariffs']