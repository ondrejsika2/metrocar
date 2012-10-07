# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CarModelManufacturer'
        db.create_table('cars_carmodelmanufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cars', ['CarModelManufacturer'])

        # Adding model 'Fuel'
        db.create_table('cars_fuel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cars', ['Fuel'])

        # Adding model 'CarType'
        db.create_table('cars_cartype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('cars', ['CarType'])

        # Adding model 'CarModel'
        db.create_table('cars_carmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarModelManufacturer'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='models', to=orm['cars.CarType'])),
            ('engine', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('seats_count', self.gf('django.db.models.fields.IntegerField')()),
            ('storage_capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('main_fuel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='main_fuel', to=orm['cars.Fuel'])),
            ('alternative_fuel', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='alternative_fuel', null=True, to=orm['cars.Fuel'])),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('cars', ['CarModel'])

        # Adding model 'CarColor'
        db.create_table('cars_carcolor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cars', ['CarColor'])

        # Adding model 'Car'
        db.create_table('cars_car', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imei', self.gf('django.db.models.fields.CharField')(unique=True, max_length=18)),
            ('authorization_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('dedicated_parking_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_echo', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('manufacture_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('mobile_number', self.gf('metrocar.utils.fields.PhoneField')(max_length=14)),
            ('registration_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_position', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('last_address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cars', to=orm['cars.CarModel'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.CarColor'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_management.MetrocarUser'], null=True, blank=True)),
            ('home_subsidiary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subsidiaries.Subsidiary'])),
        ))
        db.send_create_signal('cars', ['Car'])

        # Adding model 'FuelBill'
        db.create_table('cars_fuelbill', (
            ('accountactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.AccountActivity'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Car'])),
            ('fuel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Fuel'])),
            ('liter_count', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('cars', ['FuelBill'])

        # Adding model 'MaintenanceBill'
        db.create_table('cars_maintenancebill', (
            ('accountactivity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_management.AccountActivity'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Car'])),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('cars', ['MaintenanceBill'])

        # Adding model 'Parking'
        db.create_table('cars_parking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('places_count', self.gf('django.db.models.fields.IntegerField')()),
            ('land_registry_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('polygon', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal('cars', ['Parking'])

        # Adding model 'ParkingDescription'
        db.create_table('cars_parkingdescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('parking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Parking'])),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Car'])),
        ))
        db.send_create_signal('cars', ['ParkingDescription'])

        # Adding model 'CarPosition'
        db.create_table('cars_carposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('journey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Journey'])),
        ))
        db.send_create_signal('cars', ['CarPosition'])

        # Adding model 'Journey'
        db.create_table('cars_journey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('path', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(null=True, spatial_index=False, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='T', max_length=2)),
            ('reservation', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='journeys', null=True, to=orm['reservations.Reservation'])),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cars.Car'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_management.MetrocarUser'])),
            ('speedometer_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('speedometer_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('cars', ['Journey'])


    def backwards(self, orm):
        # Deleting model 'CarModelManufacturer'
        db.delete_table('cars_carmodelmanufacturer')

        # Deleting model 'Fuel'
        db.delete_table('cars_fuel')

        # Deleting model 'CarType'
        db.delete_table('cars_cartype')

        # Deleting model 'CarModel'
        db.delete_table('cars_carmodel')

        # Deleting model 'CarColor'
        db.delete_table('cars_carcolor')

        # Deleting model 'Car'
        db.delete_table('cars_car')

        # Deleting model 'FuelBill'
        db.delete_table('cars_fuelbill')

        # Deleting model 'MaintenanceBill'
        db.delete_table('cars_maintenancebill')

        # Deleting model 'Parking'
        db.delete_table('cars_parking')

        # Deleting model 'ParkingDescription'
        db.delete_table('cars_parkingdescription')

        # Deleting model 'CarPosition'
        db.delete_table('cars_carposition')

        # Deleting model 'Journey'
        db.delete_table('cars_journey')


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
        'cars.carposition': {
            'Meta': {'object_name': 'CarPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Journey']"}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {})
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
        'cars.fuelbill': {
            'Meta': {'object_name': 'FuelBill', '_ormbases': ['user_management.AccountActivity']},
            'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Car']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'fuel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Fuel']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'liter_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cars.journey': {
            'Meta': {'object_name': 'Journey'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Car']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'path': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'journeys'", 'null': 'True', 'to': "orm['reservations.Reservation']"}),
            'speedometer_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'speedometer_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'T'", 'max_length': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_management.MetrocarUser']"})
        },
        'cars.maintenancebill': {
            'Meta': {'object_name': 'MaintenanceBill', '_ormbases': ['user_management.AccountActivity']},
            'accountactivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['user_management.AccountActivity']", 'unique': 'True', 'primary_key': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Car']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cars.parking': {
            'Meta': {'object_name': 'Parking'},
            'cars': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cars.Car']", 'through': "orm['cars.ParkingDescription']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_registry_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'places_count': ('django.db.models.fields.IntegerField', [], {}),
            'polygon': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cars.parkingdescription': {
            'Meta': {'object_name': 'ParkingDescription'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Car']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parking': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cars.Parking']"})
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

    complete_apps = ['cars']