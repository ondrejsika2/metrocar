# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pricelist'
        db.create_table('tarification_pricelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pickup_fee', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('price_per_hour', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('price_per_km', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('reservation_fee', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('valid_from', self.gf('django.db.models.fields.DateField')()),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarModel'])),
        ))
        db.send_create_signal('tarification', ['Pricelist'])

        # Adding model 'PricelistDay'
        db.create_table('tarification_pricelistday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('weekday_from', self.gf('django.db.models.fields.SmallIntegerField')(max_length=1, null=True, blank=True)),
            ('pricelist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tarification.Pricelist'])),
        ))
        db.send_create_signal('tarification', ['PricelistDay'])

        # Adding unique constraint on 'PricelistDay', fields ['date', 'pricelist']
        db.create_unique('tarification_pricelistday', ['date', 'pricelist_id'])

        # Adding unique constraint on 'PricelistDay', fields ['weekday_from', 'pricelist']
        db.create_unique('tarification_pricelistday', ['weekday_from', 'pricelist_id'])

        # Adding model 'PricelistDayTime'
        db.create_table('tarification_pricelistdaytime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('car_unused_ratio', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('car_used_ratio', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('late_return_ratio', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('time_from', self.gf('django.db.models.fields.TimeField')()),
            ('pricelist_day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tarification.PricelistDay'])),
        ))
        db.send_create_signal('tarification', ['PricelistDayTime'])

        # Adding unique constraint on 'PricelistDayTime', fields ['time_from', 'pricelist_day']
        db.create_unique('tarification_pricelistdaytime', ['time_from', 'pricelist_day_id'])

        # Adding model 'StornoFeeTimeline'
        db.create_table('tarification_stornofeetimeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preceeding_time_from', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('tarification', ['StornoFeeTimeline'])

        # Adding model 'StornoFee'
        db.create_table('tarification_stornofee', (
            ('accountactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.AccountActivity'], unique=True, primary_key=True)),
            ('reservation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reservations.Reservation'], unique=True)),
            ('fee_timeline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tarification.StornoFeeTimeline'])),
        ))
        db.send_create_signal('tarification', ['StornoFee'])


    def backwards(self, orm):
        # Removing unique constraint on 'PricelistDayTime', fields ['time_from', 'pricelist_day']
        db.delete_unique('tarification_pricelistdaytime', ['time_from', 'pricelist_day_id'])

        # Removing unique constraint on 'PricelistDay', fields ['weekday_from', 'pricelist']
        db.delete_unique('tarification_pricelistday', ['weekday_from', 'pricelist_id'])

        # Removing unique constraint on 'PricelistDay', fields ['date', 'pricelist']
        db.delete_unique('tarification_pricelistday', ['date', 'pricelist_id'])

        # Deleting model 'Pricelist'
        db.delete_table('tarification_pricelist')

        # Deleting model 'PricelistDay'
        db.delete_table('tarification_pricelistday')

        # Deleting model 'PricelistDayTime'
        db.delete_table('tarification_pricelistdaytime')

        # Deleting model 'StornoFeeTimeline'
        db.delete_table('tarification_stornofeetimeline')

        # Deleting model 'StornoFee'
        db.delete_table('tarification_stornofee')


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
        'cars.car': {
            'Meta': {'object_name': 'Car'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authorization_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarColor']"}),
            'dedicated_parking_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_subsidiary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subsidiaries.Subsidiary']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '18'}),
            'last_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_echo': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_position': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'manufacture_date': ('django.db.models.fields.DateTimeField', [], {}),
            'mobile_number': ('metrocar.utils.fields.PhoneField', [], {'max_length': '14'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cars'", 'to': "orm['cars.CarModel']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_management.MetrocarUser']", 'null': 'True', 'blank': 'True'}),
            'registration_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'cars.carcolor': {
            'Meta': {'object_name': 'CarColor'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cars.carmodel': {
            'Meta': {'object_name': 'CarModel'},
            'alternative_fuel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alternative_fuel'", 'null': 'True', 'to': "orm['cars.Fuel']"}),
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_fuel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main_fuel'", 'to': "orm['cars.Fuel']"}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarModelManufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seats_count': ('django.db.models.fields.IntegerField', [], {}),
            'storage_capacity': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'models'", 'to': "orm['cars.CarType']"})
        },
        'cars.carmodelmanufacturer': {
            'Meta': {'object_name': 'CarModelManufacturer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'cars.cartype': {
            'Meta': {'object_name': 'CarType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cars.fuel': {
            'Meta': {'object_name': 'Fuel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reservations.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'car': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': "orm['cars.Car']"}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'path': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'default': 'None', 'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'reserved_from': ('django.db.models.fields.DateTimeField', [], {}),
            'reserved_until': ('django.db.models.fields.DateTimeField', [], {}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': "orm['user_management.MetrocarUser']"})
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
        'tarification.pricelist': {
            'Meta': {'object_name': 'Pricelist'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.CarModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pickup_fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'price_per_hour': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'price_per_km': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'reservation_fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'valid_from': ('django.db.models.fields.DateField', [], {})
        },
        'tarification.pricelistday': {
            'Meta': {'unique_together': "(('date', 'pricelist'), ('weekday_from', 'pricelist'))", 'object_name': 'PricelistDay'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tarification.Pricelist']"}),
            'weekday_from': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'tarification.pricelistdaytime': {
            'Meta': {'unique_together': "(('time_from', 'pricelist_day'),)", 'object_name': 'PricelistDayTime'},
            'car_unused_ratio': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'car_used_ratio': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'late_return_ratio': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'pricelist_day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tarification.PricelistDay']"}),
            'time_from': ('django.db.models.fields.TimeField', [], {})
        },
        'tarification.stornofee': {
            'Meta': {'object_name': 'StornoFee', '_ormbases': ['user_management.AccountActivity']},
            'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'}),
            'fee_timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tarification.StornoFeeTimeline']"}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservations.Reservation']", 'unique': 'True'})
        },
        'tarification.stornofeetimeline': {
            'Meta': {'object_name': 'StornoFeeTimeline'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preceeding_time_from': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '8', 'decimal_places': '2'})
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

    complete_apps = ['tarification']