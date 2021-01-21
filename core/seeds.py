from django.contrib.auth.models import User

from core import models
import random




def seed():
    # User
    user = User.objects.create(
        username=f"SeedCustomer{random.randint(100000,999999)}",
        password="customer@12345678",
        first_name="max",
        last_name="mustemann",
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
    print("Done!")
