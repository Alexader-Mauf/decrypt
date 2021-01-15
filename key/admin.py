from django.contrib import admin
from .models import SecretMsg
from . import models
# Register your models here.


@admin.register(models.SecretMsg)
class SecretMsgAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "message",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "pk",
        "created_at",
        "updated_at",
    )

