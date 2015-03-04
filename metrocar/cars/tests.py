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
