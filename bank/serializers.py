from rest_framework import serializers

from bank.models import BankUserAdministration
from core import models


class BankCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankCustomer
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
            'created_at',
            'updated_at',
        )


class BankTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankTransfer
        fields = (
            'id',
            'iban_from',
            'iban_to',
            'is_success',
            'is_open',
            'use_case',
            'executionlog',
            'execute_datetime',
            'amount',
            'created_at',
            'updated_at',
            'created_by',
        )

        # fields = '__all__'

        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'executionlog',
            'is_open',
            'is_success',
            'created_by',
            # 'iban_from'
        )

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = request.user
        adminstating_ibans = [x.iban for x in BankUserAdministration(user).adminstrating_accounts]
        if not validated_data['iban_from'].iban in adminstating_ibans:
            raise serializers.ValidationError({"detail": "Not an account from user"})
        validated_data['created_by'] = request.user.bank_customer
        return super(BankTransferSerializer, self).create(validated_data=validated_data)


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankAccount
        fields = (
            "name",
            "iban",
            "account_owned_by",
            "balance",
            "updated_at",
            "created_at",
        )
        read_only_fields = (
            "id",
            "iban",
            "account_owned_by",
            "balance",
            'created_at',
            'updated_at',
        )
