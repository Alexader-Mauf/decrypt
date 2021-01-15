from key import models
from . import models
from rest_framework import serializers

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BankModel
        fields = '__all__'
        read_only_fields = (
            'name',
            'vorname',
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