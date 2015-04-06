from rest_framework import serializers
from metrocar.reservations.models import Reservation, ReservationBill


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            'id', 'cancelled', 'comment', 'created', 'ended', 'finished', 'is_service',
            'modified', 'price', 'reserved_from', 'reserved_until', 'started', 'user',
            'car'
        )


# class ReservationBillSerializer(AccountActivitySerializer):
#
#     class Meta:
#         model = ReservationBill
