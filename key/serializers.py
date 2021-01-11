from key import models
from rest_framework import serializers

class SecretMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecretMsg
        fields = '__all__'
        read_only_fields = (
            'uuid',
            'created_at',
            'updated_at',
        )