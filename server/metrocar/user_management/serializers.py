from django.contrib.auth.models import User
from rest_framework import serializers
from metrocar.invoices.models import UserInvoiceAddress
from metrocar.reservations.models import ReservationBill
from metrocar.user_management.models import AccountActivity, MetrocarUser, Account, Deposit, UserRegistrationRequest


class MetrocarUserSerializer(serializers.ModelSerializer):

    active = serializers.SerializerMethodField(method_name="get_active")

    street = serializers.SerializerMethodField(method_name="get_street")

    land_registry_number = serializers.SerializerMethodField(method_name="get_land_registry_number")

    zip_code = serializers.SerializerMethodField(method_name="get_zip_code")

    city = serializers.SerializerMethodField(method_name="get_city")

    def get_active(self, obj):
        user_registration_request = UserRegistrationRequest.objects.filter(
            user=obj.id
        )
        if (user_registration_request.__len__()):
            return user_registration_request[0].approved
        else:
            return False

    def get_street(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].street
        else:
            return ""

    def get_land_registry_number(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].land_registry_number
        else:
            return ""

    def get_zip_code(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].zip_code
        else:
            return ""

    def get_city(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].city
        else:
            return ""

    class Meta:
        model = MetrocarUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'active',
            'date_of_birth',
            'drivers_licence_number',
            'identity_card_number',
            'primary_phone',
            'drivers_licence_image',
            'identity_card_image',
            'drivers_licence_image',
            'identity_card_image',
            'street',
            'land_registry_number',
            'zip_code',
            'city',
        )

class RegistrationSerializer(serializers.ModelSerializer):

    street = serializers.SerializerMethodField(method_name="get_street")

    land_registry_number = serializers.SerializerMethodField(method_name="get_land_registry_number")

    zip_code = serializers.SerializerMethodField(method_name="get_zip_code")

    city = serializers.SerializerMethodField(method_name="get_city")

    def get_street(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].street
        else:
            return ""

    def get_land_registry_number(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].land_registry_number
        else:
            return ""

    def get_zip_code(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].zip_code
        else:
            return ""

    def get_city(self, obj):
        user_invoice_address = UserInvoiceAddress.objects.filter(user=obj.id)
        if (user_invoice_address.__len__()):
            return user_invoice_address[0].city
        else:
            return ""

    class Meta:
        model = MetrocarUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'date_of_birth',
            'drivers_licence_number',
            'identity_card_number',
            'primary_phone',
            'drivers_licence_image',
            'identity_card_image',
            'street',
            'land_registry_number',
            'zip_code',
            'city',
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


