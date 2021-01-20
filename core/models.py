import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.

class BankCustomer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    adress = models.CharField(max_length=255, default="None")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def __repr__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = "Bankkunde"
        verbose_name_plural = "Bankkunden"


class BankAccount(models.Model):
    @staticmethod
    def _generate_iban():
        import random
        blz = random.randint(10000000, 99999999)
        account_nr = random.randint(10 ** 10, 9 * 10 ** 10)
        output = f"DE82{blz}{account_nr}"
        return output

    name = models.CharField(
        max_length=255,
        default=None
    )
    iban = models.CharField(
        max_length=255,
        unique=True,
        default=_generate_iban.__get__(models.Model),
    )
    account_owned_by = models.ForeignKey(
        BankCustomer,
        # related_name="bankaccounts",
        on_delete=models.CASCADE,
        verbose_name="Inhaber"
    )
    balance = models.DecimalField(
        max_digits=22,
        decimal_places=4,
        default=0.0,
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return "IBAN:{}".format(self.iban)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        if self.iban is None:
            self.iban = self._generate_iban()
        super().save(force_insert, force_update, using, update_fields)


class BankTransfer(models.Model):
    iban_from = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        verbose_name="Überweisender",
        related_name="Überweisender",
    )
    executionlog = models.TextField(default=""),
    execute_datetime = models.DateTimeField(default=()), #now is the default to be implemented
    is_open = True,
    is_success = False,
    iban_to = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        verbose_name="Begünstigter",
        related_name="Begünstigter",
    )
    amount = models.DecimalField(max_digits=22, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "IBAN:{}".fomat(self.iban)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __repr__(self):
        return "{} hat {} an {} überwiesen.".format(self.iban_from, self.amount, self.iban_to)
