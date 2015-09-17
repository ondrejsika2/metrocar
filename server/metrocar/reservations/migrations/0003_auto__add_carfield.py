# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("cars", "0004_auto__add_field_car_last_echo"),
    )

    def forwards(self, orm):
        # Adding field 'Car.last_echo'
        db.add_column('reservations_reservation', 'car',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Car'],
                                                                            related_name='reservations'),
                      keep_default=False)

        db.create_table(u'reservations_reservationreminder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reservation', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reservations.Reservation'], unique=True)),
        ))
        db.send_create_signal(u'reservations', ['ReservationReminder'])

        # Adding model 'ReservationBill'
        db.create_table(u'reservations_reservationbill', (
            (u'accountactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.AccountActivity'], unique=True, primary_key=True)),
            ('reservation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reservations.Reservation'])),
        ))
        db.send_create_signal(u'reservations', ['ReservationBill'])


        # Changing field 'Reservation.created'
        db.alter_column(u'reservations_reservation', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Reservation.modified'
        db.alter_column(u'reservations_reservation', 'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Deleting field 'Car.last_echo'
        db.delete_column('reservations_reservation', 'car')

        db.delete_table(u'reservations_reservationreminder')

        # Deleting model 'ReservationBill'
        db.delete_table(u'reservations_reservationbill')


        # Changing field 'Reservation.created'
        db.alter_column(u'reservations_reservation', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Reservation.modified'
        db.alter_column(u'reservations_reservation', 'modified', self.gf('django.db.models.fields.DateTimeField')())

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
        u'cars.car': {
            'Meta': {'object_name': 'Car'},
            '_last_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'last_address'", 'blank': 'True'}),
            '_last_position': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'db_column': "'last_position'", 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cars.CarColor']"}),
            'dedicated_parking_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_subsidiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subsidiaries.Subsidiary']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_echo': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'manufacture_date': ('django.db.models.fields.DateTimeField', [], {}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cars'", 'to': u"orm['cars.CarModel']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_management.MetrocarUser']", 'null': 'True', 'blank': 'True'}),
            'parking': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parking'", 'null': 'True', 'to': u"orm['cars.Parking']"}),
            'registration_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'cars.carcolor': {
            'Meta': {'object_name': 'CarColor'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cars.carmodel': {
            'Meta': {'object_name': 'CarModel'},
            'alternative_fuel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alternative_fuel'", 'null': 'True', 'to': u"orm['cars.Fuel']"}),
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_fuel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main_fuel'", 'to': u"orm['cars.Fuel']"}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cars.CarModelManufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seats_count': ('django.db.models.fields.IntegerField', [], {}),
            'storage_capacity': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'models'", 'to': u"orm['cars.CarType']"})
        },
        u'cars.carmodelmanufacturer': {
            'Meta': {'object_name': 'CarModelManufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'cars.cartype': {
            'Meta': {'object_name': 'CarType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'cars.fuel': {
            'Meta': {'object_name': 'Fuel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cars.parking': {
            'Meta': {'object_name': 'Parking'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_registry_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'places_count': ('django.db.models.fields.IntegerField', [], {}),
            'polygon': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reservations.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'car': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': u"orm['cars.Car']"}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'reserved_from': ('django.db.models.fields.DateTimeField', [], {}),
            'reserved_until': ('django.db.models.fields.DateTimeField', [], {}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': u"orm['user_management.MetrocarUser']"})
        },
        u'reservations.reservationbill': {
            'Meta': {'object_name': 'ReservationBill', '_ormbases': [u'user_management.AccountActivity']},
            u'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reservations.Reservation']"})
        },
        u'reservations.reservationreminder': {
            'Meta': {'object_name': 'ReservationReminder'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reservation': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['reservations.Reservation']", 'unique': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 18, 0, 0)'}),
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
        u'user_management.metrocaruser': {
            'Meta': {'object_name': 'MetrocarUser', '_ormbases': [u'auth.User']},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_management.Company']", 'null': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'drivers_licence_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100000', 'null': 'True'}),
            'drivers_licence_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'home_subsidiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subsidiaries.Subsidiary']"}),
            'identity_card_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100000', 'null': 'True'}),
            'identity_card_number': ('metrocar.utils.fields.IdentityCardNumberField', [], {'max_length': '9'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'primary_phone': ('metrocar.utils.fields.PhoneField', [], {'max_length': '14', 'null': 'True'}),
            'specific_symbol': ('django.db.models.fields.IntegerField', [], {'max_length': '12', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['reservations']
