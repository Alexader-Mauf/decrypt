from django.contrib import admin
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

@admin.register(models.BankCustomer)
class BankModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "vorname",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "pk",
        "name",
        "vorname"
,        "created_at",
        "updated_at",
    )

@admin.register(models.BankAccount)
class BankModelAdmin(admin.ModelAdmin):
    list_display = (
        "inhaber",
        "balance",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "pk",
        "created_at",
        "updated_at",
    )