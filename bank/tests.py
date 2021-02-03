import uuid
import random
from django.db import models
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import BankTransfer,BankAccount,BankCustomer
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

#content_type = ContentType.objects.get_for_model(BankTransfer)
#permission_to_add_transfers = Permission.objects.create(
#    codename='can_add_transfer',
#    name='Kann eine Überweisung beauftragen',
#    content_type=content_type,
#)
#permission_to_view_transfers = Permission.objects.create(
#    codename='can_view_transfer',
#    name='Kann eine Überweisung ansehen',
#    content_type=content_type,
#)
#content_type = ContentType.objects.get_for_model(BankCustomer)
#permission_to_view_customer = Permission.objects.create(
#    codename='can_view_customer',
#    name='Kann eine Überweisung ansehen',
#    content_type=content_type,
#)
#content_type = ContentType.objects.get_for_model(BankAccount)
#permission_to_add_accounts = Permission.objects.create(
#    codename='can_add_account',
#    name='Kann ein Konto eröffnen.',
#    content_type=content_type,
#)
#user_permissions = [permission_to_add_accounts,permission_to_add_transfers,permission_to_view_transfers,permission_to_view_customer]


#
# def testtransfer(SetUpClass):
#    sende an die transfer api einen post  request mit  json  und der  information konto from, konto to, betrag
#    also check if send konto is loged in konto also das der authorisierte benutzer nur geld von seinem konto schickt


class TestAPIEndpointAuthorization(TestCase):
    def test_api_authorization(self):
        urls = [
            'bank-customers',
            'bank-accounts',
            'bank-transfers',
        ]
        client = APIClient()
        for x in urls:
            r = client.get('/bank/api/{}/'.format(x))
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)



class Generator:

    @staticmethod
    def random_string() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def generate_user(**kwargs):
        user = User.objects.create(
            username=kwargs.get("username", f"SeedCustomer{random.randint(100000, 999999)}"),
            password=kwargs.get("asd", f"pw{random.randint(10000,999909)}"),
            first_name=kwargs.get("first_name", Generator.random_string()),
            last_name=kwargs.get("last_name", Generator.random_string()),
        )
        #user.user_permissions.set(user_permissions) # have to programm the rights manualy since the test database is always fresh
        user.save()
        return user


    @staticmethod
    def generate_customer(**kwargs):
        customer = BankCustomer(
            user=kwargs.get("user", Generator.generate_user()),
            adress=kwargs.get("adress", Generator.random_string())
        )
        customer.save()
        return customer

    @staticmethod
    def generate_account(**kwargs):
        customer = Generator.generate_customer()
        account = BankAccount(
            name=kwargs.get("name", Generator.random_string()),
            account_owned_by=kwargs.get("account_owned_by", customer),
            balance=kwargs.get("balance", 500),
        )
        account.save()
        return account

    @staticmethod
    def generate_transfer(**kwargs):
        transfer = BankTransfer(
            iban_from=kwargs.get("iban", Generator.generate_account()),
            iban_to=kwargs.get("iban", Generator.generate_account()),
            amount=13
        )
        transfer.save()
        return transfer


    #@staticmethod
    #def generate_mandant(**kwargs):
    #    mandant = models.Mandant.objects.create(
    #        name=kwargs.get("name", Generator.random_string()),
    #        agb=kwargs.get("agb", Generator.random_string()),
    #        impressum=kwargs.get("impressum", Generator.random_string()),
    #    )
    #    mandant.save()
    #    [mandant.users.add(x) for x in kwargs.get("users", [])]
    #    mandant.save()
    #    return mandant



class SetupClass(TestCase):
    admin_username = 'admin'
    admin_pwd = ':L:3M3pFK"N$Y!Qj'

    bank_customer_username = 'not_admin'
    bank_customer_pwd= ':fuckme'


    def create_bank_customer_user(self):
        #user erstellen
        user = User.objects.create(
            username=self.bank_customer_username,
            password=self.bank_customer_pwd,
            first_name=f"vorname{random.randint(100000, 999999)}",
            last_name=f"nachname{random.randint(100000, 999999)}",
        )
        user.save()
        Generator.generate_customer(user=user,adress=f"{random.randint(1,100)}te Straße, {random.randint(1,234)}")

        # gruppe
        codenames = [
            'view_banktransfer',
            'add_banktransfer',
            'view_bankaccount',
            'view_bankcustomer',
            'change_bankcustomer',

        ]
        permissions = Permission.objects.filter(codename__in=codenames).all()
        user.user_permissions = permissions

        # customer
        customer = Generator.generate_customer(user=user)
        account = Generator.generate_account(account_owned_by=customer, name="Testkonto")
        customer = get_object_or_404(customer, pk=user.id)
        # return customer



    def create_superuser(self):
        u = User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_pwd
        )
        u.save()

    def setUp(self):
        self.create_superuser()



class TestApiClass(SetupClass):
    def test_bankaccount(self):
        client = APIClient()
        client.login(username=self.bank_customer_username, password=self.bank_customer_pwd)

        bankuser = Generator.generate_customer()

        # testing accounts
        # List
        r = client.get('/core/api/bank-accounts/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        # Create
        data = {
            "name": Generator.random_string(),
            "balance": "0.0000",
            "account_owned_by": bankuser.pk
        }
        r = client.post('/core/api/bank-accounts/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        account_id = r.json().get('iban')

        # Read
        r = client.get('/core/api/bank-accounts/{}/'.format(account_id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(r.json().get("name"), data.get("name"))
        #self.assertEqual(r.json().get("balance"), data.get("balance"))
        #self.assertEqual(r.json().get("account_owned_by"), data.get("account_owned_by"))

        # Update
        data = {
            "name": Generator.random_string(),
            "balance": "1.0000",
        }
        r = client.patch(
            '/core/api/bank-accounts/{}/'.format(account_id),
            data=data,
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(r.json().get("name"), data.get("name"))
        #self.assertEqual(r.json().get("balance"), data.get("balance"))

        # Delete
        r = client.delete('/core/api/bank-accounts/{}/'.format(account_id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers(self):
        client = APIClient()
        client.login(username=self.bank_customer_username, password=self.bank_customer_pwd)

        # testing Customers
        # List
        r = client.get('/core/api/bank-customers/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        user = self.create_bank_customer_user()
        # customer = Generator.generate_customer(user=user)
        # Create
        data = {
            "adress": Generator.random_string(),
            "user": user.id
        }
        r = client.post('/core/api/bank-customers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        customer_id = r.json().get('id')

        # Read
        r = client.get('/core/api/bank-customers/{}/'.format(customer_id))

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        #self.assertEqual(r.json().get("adress"), data.get("adress"))
        #self.assertEqual(r.json().get("user"), data.get("user"))

        # Update
        data = {
            "adress": Generator.random_string(),
        }
        r = client.patch(
            '/core/api/bank-customers/{}/'.format(customer_id),
            data=data,
            format='json'
        )
        #print(client.has_perm('can_patch_account'))
        print(r)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("adress"), data.get("adress"))

        # Delete
        r = client.delete('/core/api/bank-customers/{}/'.format(customer_id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


    def test_transfers(self):
        client = APIClient()
        client.login(username=self.bank_customer_username, password=self.bank_customer_pwd)

        # testing transfers

        account_1 = Generator.generate_account()
        account_2 = Generator.generate_account()

        # List
        r = client.get('/core/api/bank-transfers/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        # Create
        data = {
            "iban_from": account_1.pk,
            "iban_to": account_2.pk,
            "is_success": False,
            "is_open": False,
            # "executionlog": "",
            "amount": '20.0000',
            "use_case": Generator.random_string(),
            "created_by": account_1.account_owned_by.pk,
        }
        r = client.post('/core/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        transfer_id = r.json().get('id')

        # Read
        r = client.get('/core/api/bank-transfers/{}/'.format(transfer_id))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("iban_from"), data.get("iban_from"))
        self.assertEqual(r.json().get("iban_to"),data.get("iban_to"))
        self.assertEqual(r.json().get("amount"), data.get("amount"))
        self.assertEqual(r.json().get("is_open"), data.get("is_open"))
        self.assertEqual(r.json().get("is_success"), data.get("is_success"))



        # Update
        data = {
            "is_open": False,
            "is_success": True,
            }
        r = client.patch(
            '/core/api/bank-transfers/{}/'.format(transfer_id),
            data=data,
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
       # self.assertEqual(r.json().get("is_open"), data.get("is_open"))
       # self.assertEqual(r.json().get("is_success"), data.get("is_success"))
        # wäre es sinnvoll, wenn man self.assertEqual(None,data.get("is_open")) benutzt zum doppelcheck?

        # Delete
        r = client.delete('/core/api/bank-accounts/{}/'.format(transfer_id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


