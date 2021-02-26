from django.contrib import admin
from . import models
# Register your models here.


def execute_transfer(modeladmin, request, queryset):
    for entry in queryset:
        entry.run_transfer()
    execute_transfer.short_description = "führt mögliche Überweisungen aus"




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
        "use_case",
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
        "use_case",
        "created_at",
        "updated_at",
    )
    select_related = (
        'iban_from',
    )
    actions = [execute_transfer]
