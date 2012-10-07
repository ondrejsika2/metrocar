# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('user_management_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('ic', self.gf('metrocar.utils.fields.IcField')(max_length=8, null=True)),
            ('dic', self.gf('metrocar.utils.fields.DicField')(max_length=12, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=6, null=True)),
            ('land_registry_number', self.gf('django.db.models.fields.CharField')(max_length=6, null=True)),
        ))
        db.send_create_signal('user_management', ['Company'])

        # Adding model 'MetrocarUser'
        db.create_table('user_management_metrocaruser', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('drivers_licence_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('identity_card_number', self.gf('metrocar.utils.fields.IdentityCardNumberField')(max_length=9)),
            ('primary_phone', self.gf('metrocar.utils.fields.PhoneField')(max_length=14, null=True, blank=True)),
            ('secondary_phone', self.gf('metrocar.utils.fields.PhoneField')(max_length=14, null=True, blank=True)),
            ('variable_symbol', self.gf('django.db.models.fields.IntegerField')(max_length=12, null=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_management.Company'], null=True, blank=True)),
            ('home_subsidiary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subsidiaries.Subsidiary'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('user_management', ['MetrocarUser'])

        # Adding model 'UserRegistrationRequest'
        db.create_table('user_management_userregistrationrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_registration_request', unique=True, to=orm['user_management.MetrocarUser'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resolved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('user_management', ['UserRegistrationRequest'])

        # Adding model 'UserCard'
        db.create_table('user_management_usercard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=8)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 7, 0, 0))),
            ('registration_number', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('is_service_card', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_card', unique=True, to=orm['user_management.MetrocarUser'])),
        ))
        db.send_create_signal('user_management', ['UserCard'])

        # Adding model 'Account'
        db.create_table('user_management_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=3)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='account', unique=True, to=orm['user_management.MetrocarUser'])),
        ))
        db.send_create_signal('user_management', ['Account'])

        # Adding model 'AccountActivity'
        db.create_table('user_management_accountactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activities', to=orm['user_management.Account'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 7, 0, 0))),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('money_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('account_balance', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=8, decimal_places=2)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('credited', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('user_management', ['AccountActivity'])

        # Adding model 'Deposit'
        db.create_table('user_management_deposit', (
            ('accountactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.AccountActivity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('user_management', ['Deposit'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('user_management_company')

        # Deleting model 'MetrocarUser'
        db.delete_table('user_management_metrocaruser')

        # Deleting model 'UserRegistrationRequest'
        db.delete_table('user_management_userregistrationrequest')

        # Deleting model 'UserCard'
        db.delete_table('user_management_usercard')

        # Deleting model 'Account'
        db.delete_table('user_management_account')

        # Deleting model 'AccountActivity'
        db.delete_table('user_management_accountactivity')

        # Deleting model 'Deposit'
        db.delete_table('user_management_deposit')


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
        'user_management.deposit': {
            'Meta': {'object_name': 'Deposit', '_ormbases': ['user_management.AccountActivity']},
            'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'})
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
        },
        'user_management.usercard': {
            'Meta': {'object_name': 'UserCard'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_service_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 10, 7, 0, 0)'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_card'", 'unique': 'True', 'to': "orm['user_management.MetrocarUser']"})
        },
        'user_management.userregistrationrequest': {
            'Meta': {'object_name': 'UserRegistrationRequest'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_registration_request'", 'unique': 'True', 'to': "orm['user_management.MetrocarUser']"})
        }
    }

    complete_apps = ['user_management']