from rest_framework import serializers
from metrocar.cars.models import Car, CarModel, CarColor, FuelBill, Journey, Parking


class CarSerializer(serializers.ModelSerializer):

    car_name = serializers.SerializerMethodField(method_name="get_car_name")

    def get_car_name(self, obj):
        return obj.model.name + ' ' + obj.color.color

    class Meta:
        model = Car
        fields = (
            'id',
            'active',
            'dedicated_parking_only',
            'manufacture_date',
            'registration_number',
            'image',
            'model',
            'color',
            'owner',
            'home_subsidiary',
            'last_echo',
            '_last_position',
            '_last_address',
            'parking',
            'car_name'
        )


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = (
            'id', 'name', 'manufacturer', 'type', 'engine', 'seats_count', 'storage_capacity', 'main_fuel', 'alternative_fuel','notes', 'image'
        )


class CarColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarColor
        fields = (
            'id', 'color'
        )


class FuelBillSerializer(serializers.ModelSerializer):

    def validate_approved(self, attrs, source):
        if attrs[source]:
            raise serializers.ValidationError('Changes of approved flag is allowed only from django administration')
        return attrs


    class Meta:
        model = FuelBill
        fields = (
            'id',
            'account',
            'money_amount',
            'car',
            'fuel',
            'liter_count',
            'place',
            'image',
            'approved',
        )

class JourneySerializer(serializers.ModelSerializer):

    class Meta:
        model = Journey
        fields = (

        )

class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = (
            'id',
            'name',
            'places_count',
            'land_registry_number',
            'street',
            'city',
            'polygon',
        )