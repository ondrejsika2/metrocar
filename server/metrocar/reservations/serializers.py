from rest_framework import serializers
from metrocar.reservations.models import Reservation, ReservationBill


class ReservationSerializer(serializers.ModelSerializer):
    datafile = serializers.Field()

    class Meta:
        model = Reservation
        fields = (
            'id',
            'cancelled',
            'comment',
            'created',
            'ended',
            'finished',
            'modified',
            'price',
            'reserved_from',
            'reserved_until',
            'started',
            'user',
            'car',
            'datafile'
        )

# class ReservationBillSerializer(AccountActivitySerializer):
#
#     class Meta:
#         model = ReservationBill
