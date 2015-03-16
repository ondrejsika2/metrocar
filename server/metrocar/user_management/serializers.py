from django.contrib.auth.models import User
from rest_framework import serializers
from metrocar.user_management.models import AccountActivity, MetrocarUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetrocarUser
        fields = ('id', 'gender')


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        fields = (
            'account',
            'datetime',
            'comment',
            'money_amount',
            'account_balance',
            'content_type',
            'credited',
        )