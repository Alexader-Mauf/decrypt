from datetime import datetime

from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone


# Create your models here.

class BankCustomer(models.Model):
    user = models.OneToOneField(
        User,
        related_name='bank_customer',
        on_delete=models.CASCADE
    )
    adress = models.CharField(max_length=255, default="None")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = "Bankkunde"
        verbose_name_plural = "Bankkunden"

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def __repr__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


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
    administrated_by = models.ManyToManyField(
        BankCustomer,
        related_name='administrating_accounts',
        default=None
    )
    account_owned_by = models.ForeignKey(
        BankCustomer,
        # default=BankCustomer.user.username,
        related_name="account_owned_by",
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

    def save(self, *args, **kwargs):
        if self.iban is None:
            self.iban = self._generate_iban()
        super(BankAccount, self).save(*args, **kwargs)

def one_day_from_now():
    return timezone.now()+timezone.timedelta(days=1)

class BankTransfer(models.Model):
    iban_from = models.ForeignKey(
        BankAccount,
        on_delete=models.ProtectedError,
        verbose_name="Überweisender",
        related_name="Überweisender",
    )
    created_by = models.ForeignKey(
        BankCustomer,
        on_delete=models.DO_NOTHING,
        verbose_name="Auftraggeber",
        related_name="created_by"

    )
    use_case = models.TextField(
        verbose_name="Verwendungszweck",
    )
    executionlog = models.TextField(
        default="erstellt",
    )

    execute_datetime = models.DateTimeField(
        default=one_day_from_now()
    )

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
                # amount must be positive
                if self.amount < 0:
                    self.executionlog += (" Error: kann keine negativen beträge überweisen.")
                    self.is_open = False
                    self.save()
                    print("negativer amount")
                    return

                # transfer darf nicht schon angesetzt wurden sein
                if self.is_open == False:
                    self.executionlog += (" Error: dieser Auftrag wurde schon angesetzt")
                    self.save()
                    return

                # Zielaccount darf nicht Absendeaccount sein
                if account_from == account_to:
                    self.executionlog = self.executionlog + " Error: Kann keine Überweisung an das Absenderkonto ausführen."
                    self.is_open = False
                    self.save()
                    print("gleicher account")
                    return

                # man darf nicht mehr überweisen, als man geld auf dem Konto hat
                if account_from.balance > amount:
                    print("starting  transaction")
                    self.iban_from.balance = self.iban_from.balance - self.amount
                    self.iban_to.balance = self.iban_to.balance + self.amount
                    self.iban_to.save()
                    self.iban_from.save()
                    self.executionlog = self.executionlog + "Sucess: überweisung ausgeführt"
                    # change
                    self.is_open = False
                    self.is_success = True
                    self.save()
                else:
                    print("nicht genug guthaben")
                    self.is_open = False
                    self.executionlog = self.executionlog + " Error: Nicht genug Guthaben."
                    self.save()
        except Exception as e:
            print(e)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self) -> str:
        return str(self.pk)

    def __repr__(self) -> str:
        return "{}".format(self.pk)


class RepeatedTransaction(models.Model):
    transaction_to_be_repeated = models.ForeignKey(
        BankTransfer,
        related_name="to_be_repeated",
        verbose_name="Dauerauftrag",
        on_delete=models.DO_NOTHING
    )
    starting_date = models.DateTimeField

    REPETITIONS_CHOICES = [
        ("weekly", "Wöchentlich"),
        ("monthly", "Monatlich"),
        ("yearly", "Jährlich")
    ]
    frequency = models.CharField(
        max_length=7,
        choices=REPETITIONS_CHOICES,
        default="monthly"
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def run_repeated_transaction(self):
        # create a new trransaction that is sceduled 1 frequency later then the last one
        return None
