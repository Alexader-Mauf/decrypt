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
    adress = models.CharField(max_length=255,  default="None")
    email = models.EmailField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Der Kunde von: {} {}".fomat(self.name, self.vorname)

    def __repr__(self):
        return "Der Kunde von: {} {}".fomat(self.name, self.vorname)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = "Bankkunde"
        verbose_name_plural = "Bankkunden"


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
    balance = models.DecimalField(max_digits=22, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "IBAN:{}".fomat(self.iban)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
