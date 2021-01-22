from rest_framework import serializers, status
from rest_framework.decorators import action

from . import models


class BankCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankCustomer
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
        )


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankAccount
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
        )


#class BankAccountpdateSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = models.BankAccount
#        fields = ("name", "iban", "balance",)
#        read_only_fields = (
#            'iban',
#            'balance',
#        )


class BankTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankTransfer
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
        )


class RunTransferSerializer(serializers.Serializer):
    pass