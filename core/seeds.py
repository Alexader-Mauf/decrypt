from django.contrib.auth.models import User

from core import models
import random




def seed():
    # User
    user = User.objects.create(
        username=f"SeedCustomer{random.randint(100000,999999)}",
        password="customer@12345678",
        first_name=f"vorname{random.randint(100000, 999999)}",
        last_name=f"nachname{random.randint(100000, 999999)}",
    )
    user.save()
    # BankCustomer
    customer = models.BankCustomer.objects.create(
        user=user,
        adress="",
    )
    customer.save()

    account = models.BankAccount.objects.create(
        name="geld",
        account_owned_by=customer
    )
    account.save()

    user = User.objects.create(
        username=f"SeedCustomer{random.randint(100000, 999999)}",
        password="customer@12345678",
        first_name=f"vorname{random.randint(100000, 999999)}",  # muss durch genérator erzeugt werden
        last_name=f"nachname{random.randint(100000, 999999)}",  # muss durch generator  erzeugt  werden
    )

    customer2 = models.BankCustomer.objects.create(
        user=user,
        adress="",
    )
    customer2.save()

    account2 = models.BankAccount.objects.create(
        name="geld",
        account_owned_by=customer2
    )
    account2.save()

    transfer = models.BankTransfer.objects.create(
        iban_from=account2,
        amount=20,
        iban_to=account,

    )
    transfer.save()
    print("Done!")
