import datetime
import uuid
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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        customer = BankCustomer.objects.create(user=instance)
        BankAccount.objects.create(
            account_owned_by=customer,
        )


class BankAccount(models.Model):
    name = models.CharField(
        max_length=255,
    )
    iban = models.CharField(
        max_length=255,
        unique=True
    )
    account_owned_by = models.ForeignKey(
        BankCustomer,
        related_name="bankaccounts",
        on_delete=models.CASCADE,
        verbose_name="Inhaber"
    )
    balance = models.DecimalField(
        max_digits=22,
        decimal_places=4,
        default=0.0
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def _generate_iban():
        import random
        blz = random.randint(10000000, 99999999)
        account_nr = random.randint(10 ** 10, 9 * 10 ** 10)
        output = f"DE82{blz}{account_nr}"
        return output

    def __init__(self):
        self.iban = self._generate_iban()

    def __str__(self):
        return "IBAN:{}".format(self.iban)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        if self.iban is None:
            self.iban = self._generate_iban()
        super(BankAccount, self).save(*args, **kwargs)


class BankTransfer(models.Model):
    iban_from = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        verbose_name="Überweisender",
        related_name="Überweisender",
    )
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
