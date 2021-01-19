from key import models
from . import models
from rest_framework import serializers

class BankCustomerSerializer(serializers.ModelSerializer):
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
class BankTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankTransfer
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
        )


class SecretMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecretMsg
        fields = '__all__'
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
        )