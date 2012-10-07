# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyInvoiceAddress'
        db.create_table('invoices_companyinvoiceaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('land_registry_number', self.gf('django.db.models.fields.IntegerField')(max_length=8)),
            ('house_number', self.gf('django.db.models.fields.IntegerField')(max_length=8, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('state', self.gf('django.db.models.fields.CharField')(default=u'Czech Republic', max_length=100)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('company', self.gf('django.db.models.fields.related.OneToOneField')(related_name='invoice_address', unique=True, to=orm['user_management.Company'])),
            ('ic', self.gf('metrocar.utils.fields.IcField')(max_length=8, null=True)),
            ('dic', self.gf('metrocar.utils.fields.DicField')(max_length=12, null=True)),
        ))
        db.send_create_signal('invoices', ['CompanyInvoiceAddress'])

        # Adding model 'UserInvoiceAddress'
        db.create_table('invoices_userinvoiceaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('land_registry_number', self.gf('django.db.models.fields.IntegerField')(max_length=8)),
            ('house_number', self.gf('django.db.models.fields.IntegerField')(max_length=8, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('state', self.gf('django.db.models.fields.CharField')(default=u'Czech Republic', max_length=100)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='invoice_address', unique=True, to=orm['user_management.MetrocarUser'])),
        ))
        db.send_create_signal('invoices', ['UserInvoiceAddress'])

        # Adding model 'PaymentMethod'
        db.create_table('invoices_paymentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleteable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('invoices', ['PaymentMethod'])

        # Adding model 'Invoice'
        db.create_table('invoices_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('draw_date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('variable_symbol', self.gf('django.db.models.fields.IntegerField')(max_length=12)),
            ('specific_symbol', self.gf('django.db.models.fields.IntegerField')(max_length=12)),
            ('payment_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_management.MetrocarUser'])),
            ('pdf_invoice', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('invoices', ['Invoice'])

        # Adding model 'InvoiceItem'
        db.create_table('invoices_invoiceitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_activity', self.gf('django.db.models.fields.related.OneToOneField')(related_name='invoice_item', unique=True, to=orm['user_management.AccountActivity'])),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['invoices.Invoice'])),
        ))
        db.send_create_signal('invoices', ['InvoiceItem'])


    def backwards(self, orm):
        # Deleting model 'CompanyInvoiceAddress'
        db.delete_table('invoices_companyinvoiceaddress')

        # Deleting model 'UserInvoiceAddress'
        db.delete_table('invoices_userinvoiceaddress')

        # Deleting model 'PaymentMethod'
        db.delete_table('invoices_paymentmethod')

        # Deleting model 'Invoice'
        db.delete_table('invoices_invoice')

        # Deleting model 'InvoiceItem'
        db.delete_table('invoices_invoiceitem')


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
        'invoices.companyinvoiceaddress': {
            'Meta': {'object_name': 'CompanyInvoiceAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'invoice_address'", 'unique': 'True', 'to': "orm['user_management.Company']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dic': ('metrocar.utils.fields.DicField', [], {'max_length': '12', 'null': 'True'}),
            'house_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'ic': ('metrocar.utils.fields.IcField', [], {'max_length': '8', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_registry_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'Czech Republic'", 'max_length': '100'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        'invoices.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'draw_date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pdf_invoice': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'specific_symbol': ('django.db.models.fields.IntegerField', [], {'max_length': '12'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_management.MetrocarUser']"}),
            'variable_symbol': ('django.db.models.fields.IntegerField', [], {'max_length': '12'})
        },
        'invoices.invoiceitem': {
            'Meta': {'object_name': 'InvoiceItem'},
            'account_activity': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'invoice_item'", 'unique': 'True', 'to': "orm['user_management.AccountActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['invoices.Invoice']"})
        },
        'invoices.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'deleteable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'invoices.userinvoiceaddress': {
            'Meta': {'object_name': 'UserInvoiceAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'house_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_registry_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'Czech Republic'", 'max_length': '100'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'invoice_address'", 'unique': 'True', 'to': "orm['user_management.MetrocarUser']"}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
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

    complete_apps = ['invoices']