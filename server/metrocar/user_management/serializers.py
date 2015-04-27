from django.contrib.auth.models import User
from rest_framework import serializers
from metrocar.reservations.models import ReservationBill
from metrocar.user_management.models import AccountActivity, MetrocarUser, Account, Deposit, UserRegistrationRequest


class MetrocarUserSerializer(serializers.ModelSerializer):

    active = serializers.SerializerMethodField(method_name="get_active")

    def get_active(self, obj):
        user_registration_request = UserRegistrationRequest.objects.filter(
            user=obj.id
        )
        if (user_registration_request.__len__()):
            return user_registration_request[0].approved
        else:
            return False

    class Meta:
        model = MetrocarUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'active',
            'date_of_birth',
            'drivers_licence_number',
            'identity_card_number',
            'primary_phone',
            'drivers_licence_image',
            'identity_card_image',
        )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'balance',
            'user',
        )

class AccountActivitySerializer(serializers.ModelSerializer):

    activity_type=serializers.SerializerMethodField(method_name='get_activity_type')

    def get_activity_type(self, obj):
        return obj.__class__.__name__

    class Meta:
        model=AccountActivity
        fields = (
            'id',
            'datetime',
            'money_amount',
            'activity_type',
        )


class ReservationBillSerializer(AccountActivitySerializer):

    activity_type=serializers.SerializerMethodField(method_name='get_activity_type')

    def get_activity_type(self, obj):
        print obj.datetime
        return obj.__class__.__name__

    class Meta:
        model=ReservationBill
        fields = (
            'id',
            'datetime',
            'money_amount',
            'activity_type',
        )


class DepositSerializer(AccountActivitySerializer):

    activity_type=serializers.SerializerMethodField(method_name='get_activity_type')

    def get_activity_type(self, obj):
        return obj.__class__.__name__

    class Meta:
        model=Deposit
        fields = (
            'id',
            'datetime',
            'money_amount',
            'activity_type',
        )


class FuelBillSerializer(serializers.ModelSerializer):

    activity_type=serializers.SerializerMethodField(method_name='get_activity_type')

    def get_activity_type(self, obj):
        return obj.__class__.__name__

    class Meta:
        model=Deposit
        fields = (
            'id',
            'datetime',
            'money_amount',
            'activity_type',
        )


