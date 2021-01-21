from rest_framework import serializers

from core import models


class BankCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankCustomer
        fields = (
            'pk',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'pk',
            'created_at',
            'updated_at',
        )


class BankTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankTransfer
        fields = (
            'pk',
            'iban_from',
            'iban_to',
            'is_success',
            'is_open',
            'executionlog',
            'execute_datetime',
            'amount',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'pk',
            'created_at',
            'updated_at',
        )


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankAccount
        fields = (
            'pk',
            "name",
            "iban",
            "account_owned_by",
            "balance",
            "updated_at",
            "created_at",
        )
        read_only_fields = (
            "pk",
            "name",
            "iban",
            "account_owned_by",
            "balance",
            'created_at',
            'updated_at',
        )

