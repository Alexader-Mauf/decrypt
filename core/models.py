from django.db import models
import datetime
from django.utils import timezone
import uuid


# Create your models here.

class SecretMsg(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    message = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class BankCustomer(models.Model):
    name = models.TextField(max_length=255)
    vorname = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    adress = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return "Der Kunde von: {} {}".fomat(self.name, self.vorname)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class BankAccount(models.Model):
    name=models.CharField(
        max_length=255,
    )
    iban = models.CharField(
        max_length=255,
        unique=True
    )
    inhaber = models.ForeignKey(
        BankCustomer,
        on_delete=models.CASCADE,
        verbose_name="bankkonten"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(max_digits=22, decimal_places=4)

    def __str__(self):
        return "IBAN:{}".fomat(self.iban)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
