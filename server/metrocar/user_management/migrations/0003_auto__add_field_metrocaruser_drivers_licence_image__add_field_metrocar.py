# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MetrocarUser.drivers_licence_image'
        db.add_column(u'user_management_metrocaruser', 'drivers_licence_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MetrocarUser.identity_card_image'
        db.add_column(u'user_management_metrocaruser', 'identity_card_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MetrocarUser.drivers_licence_image'
        db.delete_column(u'user_management_metrocaruser', 'drivers_licence_image')

        # Deleting field 'MetrocarUser.identity_card_image'
        db.delete_column(u'user_management_metrocaruser', 'identity_card_image')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'subsidiaries.subsidiary': {
            'Meta': {'object_name': 'Subsidiary'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'house_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_account_balance': ('django.db.models.fields.DecimalField', [], {'default': "'15000'", 'max_digits': '8', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'default': '21'}),
            'use_onboard_unit': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'user_management.account': {
            'Meta': {'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'account'", 'unique': 'True', 'to': u"orm['user_management.MetrocarUser']"})
        },
        u'user_management.accountactivity': {
            'Meta': {'object_name': 'AccountActivity'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': u"orm['user_management.Account']"}),
            'account_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '8', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'credited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 19, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'user_management.company': {
            'Meta': {'object_name': 'Company'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'dic': ('metrocar.utils.fields.DicField', [], {'max_length': '12', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'ic': ('metrocar.utils.fields.IcField', [], {'max_length': '8', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_registry_number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'user_management.deposit': {
            'Meta': {'object_name': 'Deposit', '_ormbases': [u'user_management.AccountActivity']},
            u'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'user_management.metrocaruser': {
            'Meta': {'object_name': 'MetrocarUser', '_ormbases': [u'auth.User']},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_management.Company']", 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'drivers_licence_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'drivers_licence_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'home_subsidiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subsidiaries.Subsidiary']"}),
            'identity_card_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'identity_card_number': ('metrocar.utils.fields.IdentityCardNumberField', [], {'max_length': '9'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'primary_phone': ('metrocar.utils.fields.PhoneField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'secondary_phone': ('metrocar.utils.fields.PhoneField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'specific_symbol': ('django.db.models.fields.IntegerField', [], {'max_length': '12', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'user_management.usercard': {
            'Meta': {'object_name': 'UserCard'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_service_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 19, 0, 0)'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_card'", 'unique': 'True', 'to': u"orm['user_management.MetrocarUser']"})
        },
        u'user_management.userregistrationrequest': {
            'Meta': {'object_name': 'UserRegistrationRequest'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_registration_request'", 'unique': 'True', 'to': u"orm['user_management.MetrocarUser']"})
        }
    }

    complete_apps = ['user_management']