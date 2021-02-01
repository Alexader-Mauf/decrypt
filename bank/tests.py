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


class SetupClass(TestCase):
    username = 'admin'
    pwd = ':L:3M3pFK"N$Y!Qj'

    def create_superuser(self):
        u = User.objects.create_superuser(
            username=self.username,
            password=self.pwd
        )
        u.save()

    def setUp(self):
        self.create_superuser()


class Generator:

    @staticmethod
    def random_string() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def generate_user(**kwargs):
        user = User.objects.create(
            username=f"SeedCustomer{random.randint(100000, 999999)}",
            password="customer@12345678",
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
            adress=Generator.random_string()
        )
        customer.save()
        return customer

    @staticmethod
    def generate_account(**kwargs):
        customer = Generator.generate_customer()
        account = BankAccount(
            name=Generator.random_string(),
            account_owned_by=customer,
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


class TestApiClass(SetupClass):
    def test_bankaccount(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

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
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        account_id = r.json().get('iban')

        # Read
        r = client.get('/core/api/bank-accounts/{}/'.format(account_id))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("name"), data.get("name"))
        self.assertEqual(r.json().get("balance"), data.get("balance"))
        self.assertEqual(r.json().get("account_owned_by"), data.get("account_owned_by"))

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
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("name"), data.get("name"))
        self.assertEqual(r.json().get("balance"), data.get("balance"))

        # Delete
        r = client.delete('/core/api/bank-accounts/{}/'.format(account_id))
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_customers(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        # testing Customers
        # List
        r = client.get('/core/api/bank-customers/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        user = Generator.generate_user()
        # customer = Generator.generate_customer(user=user)
        # Create
        data = {
            "adress": Generator.random_string(),
            "user": user.id
        }
        r = client.post('/core/api/bank-customers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        customer_id = r.json().get('id')

        # Read
        r = client.get('/core/api/bank-customers/{}/'.format(customer_id))

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("adress"), data.get("adress"))
        self.assertEqual(r.json().get("user"), data.get("user"))

        # Update
        data = {
            "adress": Generator.random_string(),
        }
        r = client.patch(
            '/core/api/bank-customers/{}/'.format(customer_id),
            data=data,
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("adress"), data.get("adress"))
        # self.assertEqual(r.json().get("state_from_send_message_defaults", {}).get("Offen"), False)

        # Delete
        r = client.delete('/core/api/bank-customers/{}/'.format(customer_id))
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)


    def test_transfers(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        # testing transfers

        account_1 = Generator.generate_account()
        account_2 = Generator.generate_account()

        # List
        r = client.get('/core/api/bank-transfers/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Create
        data = {
            'iban_from': account_1.iban,
            'iban_to': account_2.iban,
            'amount': "200.0000",
            'is_open': True,
            'is_success': False,
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
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("is_open"), data.get("is_open"))
        self.assertEqual(r.json().get("is_success"), data.get("is_success"))

        # Delete
        r = client.delete('/core/api/bank-accounts/{}/'.format(transfer_id))
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


