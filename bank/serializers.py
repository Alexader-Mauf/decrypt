from rest_framework import serializers

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
        fields = '__all__'
            #'id',
            #'iban_from',
            #'iban_to',
            #'is_success',
            #'is_open',
            #'use_case',
            #'executionlog',
            #'execute_datetime',
            #'amount',
            #'created_at',
            #'updated_at',
            #'created_by',

        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )


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
            "name",
            "iban",
            "account_owned_by",
            "balance",
            'created_at',
            'updated_at',
        )

