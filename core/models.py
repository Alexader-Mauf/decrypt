from datetime import datetime
from django.contrib.auth.models import User
from django.db import models, transaction
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
        primary_key=True,
        max_length=255,
        unique=True,
        default=_generate_iban.__get__(models.Model),
        verbose_name="IBAN",
    )
    account_owned_by = models.ForeignKey(
        BankCustomer,
        #default=BankCustomer.user.username,
        related_name="bankaccounts",
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
    executionlog = models.CharField(
            max_length=255,
            default=["erstellt"],
    )

    execute_datetime = models.DateTimeField(
        default=(datetime.now())
        ) #now is the default to be implemented

    is_open = models.BooleanField(
        default=True,
        )
    is_success = models.BooleanField(
        default=False,
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

    def run_transfer(self):
        try:
            with transaction.atomic():
                account_from = self.iban_from
                account_to = self.iban_to
                amount = self.amount
                # do the transaction

                ## Checks if transaction is possible
                # user must be admin
                if  self.is_open == False:
                    self.executionlog += (" Error: dieser Auftrag wurde schon angesetzt")
                    self.save()
                    return

                if account_from == account_to:
                    self.executionlog += (" Error: Kann keine Überweisung an das selbe Koto ausführen.",)
                    self.is_open = False
                    self.save()
                    print("gleicher account")



                if account_from.balance > amount:
                    print("starting  transaction")
                    self.iban_from.balance = self.iban_from.balance - self.amount
                    self.iban_to.balance = self.iban_to.balance + self.amount
                    self.iban_to.save()
                    self.iban_from.save()
                    self.executionlog += ("Sucess: überweisung ausgeführt")
                    # change
                    self.is_open = False
                    self.is_success = True
                    self.save()
                else:
                    print("nicht genug guthaben")
                    self.is_open = False
                    self.executionlog += ("Nicht genug Guthaben.")
                    self.save()

        except Exception as e:
            print(e)

    def __str__(self):
        return str(self.pk)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __repr__(self):
        return self.pk