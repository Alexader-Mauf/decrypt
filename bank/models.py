from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from core import models


# Create your models here.

class BankUserAdministration:
    def __init__(self, user: User):
        self.bank_customer = models.BankCustomer.objects.get(user=user)

    @property
    def owned_accounts(self):
        return models.BankAccount.objects.filter(
            account_owned_by=self.bank_customer
        ).all()

    @property
    def adminstrating_accounts(self):
        return models.BankAccount.objects.filter(
            Q(account_owned_by=self.bank_customer) |
            Q(administrated_by=self.bank_customer)
        ).all()
