from rest_framework import serializers
from metrocar.cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id', 'active', 'dedicated_parking_only', 'manufacture_date', 'registration_number', 'image',
            'model', 'color', 'owner', 'home_subsidiary', 'last_echo', '_last_position', '_last_address'
        )
