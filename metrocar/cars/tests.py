import unittest
from xmlrpclib import Error

from django.test import TestCase

from metrocar.tests import utils
from metrocar.cars.models import *

def create_cars_dummy_models():
	manufacturer = CarModelManufacturer.objects.create(slug='slug', title='title')
	type = CarType.objects.create(type='type')
	fuel = Fuel.objects.create(title='title')
	car_model = CarModel.objects.create(
		engine='engine', seats_count=1, storage_capacity=1, title='title',
		type=type, main_fuel=fuel, manufacturer=manufacturer
	)
	return manufacturer, type, fuel, car_model

class CarsTest(unittest.TestCase):
	server = utils.get_server()

	def test_cars_type_manipulation(self):
		"""
		Tests manipulation with car types
		"""
		
		list_pre = self.server.cars.car_type_list(True)

		ct1 = self.server.cars.car_type_edit({'type' : 'Sedan',})
		ct2 = self.server.cars.car_type_edit({'type' : 'Combi',})
		ct3 = self.server.cars.car_type_edit({'type' : 'Kabriolet',})
		
		list_after = self.server.cars.car_type_list(True)

		self.failUnlessEqual(list_pre['count'], list_after['count'] - 3)

		ct1_data = self.server.cars.car_type_get(ct1)

		self.failUnlessEqual(ct1_data[0]['pk'], ct1)
		self.failUnless(ct1_data[0]['fields']['type'], 'Sedan')


	
		self.server.cars.car_type_edit({'type' : 'Kombajn',}, ct1)
		ct1_data = self.server.cars.car_type_get(ct1)
		if (ct1_data[0]['fields']['type'] != 'Kombajn'):
				self.fail(ct1_data[0]['fields']['type'] + ' != Kombajn')


		self.failUnlessEqual(self.server.cars.car_type_delete(ct2), True)

		list_after = self.server.cars.car_type_list(True)
		
		self.failUnlessEqual(list_after['count'], list_pre['count'] + 2)

	def test_fuel_manipulation(self):
		"""
		Test manipulation with fuel
		"""

		list_pre = self.server.cars.fuel_list(True)

		f1 = self.server.cars.fuel_edit({'title' : 'benzin'})
		f2 = self.server.cars.fuel_edit({'title' : 'plyn'})
		f3 = self.server.cars.fuel_edit({'title' : 'nakadah'})

		list_after = self.server.cars.fuel_list(True)

		self.failUnlessEqual(list_pre['count'], list_after['count'] - 3)

		pass

	def test_cars_model(self):
		"""
		bla
		"""

		# creates some manufacturers
		m1 = self.server.cars.car_model_manufacturer_edit({
				'slug' : 'Skodovka',
				'title' : 'Skoda',
			})

		m2 = self.server.cars.car_model_manufacturer_edit({
				'slug' : 'Tatrovka',
				'title' : 'Tatra',
			})

		m3 = self.server.cars.car_model_manufacturer_edit({
				'slug' : 'BMW',
				'title' : 'BMW',
			})
	
		self.failIfEqual(m1, 0)
		self.failIfEqual(m2, 0)
		self.failIfEqual(m3, 0)

		m1_ret = self.server.cars.car_model_manufacturer_edit({
			'slug' : 'Skodarna',
			'title' : 'Skodovka',
		}, m1)

		self.failUnless(m1_ret, m1)

		m1_obj = self.server.cars.car_model_manufacturer_get(m1)
		self.failUnless(m1_obj[0]['fields']['slug'], 'Skodarna')
		self.failUnless(m1_obj[0]['fields']['title'], 'Skodovka')


		car_type_1 = self.server.cars.car_type_edit({'type' : 'Sedanek'})
		fuel_1 = self.server.cars.fuel_edit({'title' : 'Benzin'})

		cm1_ret = self.server.cars.car_model_edit({
				'engine' : 'motor',
				'notes' : 'poznamky',
				'seats_count' : 13434,
				'storage_capacity' : 23,
				'title' : 'modylek',
			}, fuel_1, m1, car_type_1)

		self.failIfEqual(cm1_ret, 0)




if __name__ == '__main__':
    unittest.main()
