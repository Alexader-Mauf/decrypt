from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.BankCustomer)
class BankCustomerAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "created_at",
        "updated_at",
        "adress",
    )
    readonly_fields = (
        "pk",
        "created_at",
        "updated_at",
    )
    select_related = ("user",)

@admin.register(models.BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'iban',
        "account_owned_by",
        "balance",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "pk",
        "created_at",
        "account_owned_by",
        "updated_at",
    )
    select_related = (
        'account_owned_by',
    )

@admin.register(models.BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display = (
        "iban_from",
        "iban_to",
        "amount",
        "created_at",
        "updated_at",
        "is_success",
        "is_open",
        "executionlog",
        "execute_datetime"
    )
    readonly_fields = (
        "pk",
        "created_at",
        "updated_at",
    )