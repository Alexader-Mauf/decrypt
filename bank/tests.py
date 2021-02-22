import random
import uuid

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import BankTransfer, BankAccount, BankCustomer

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
            first_name=kwargs.get("first_name", Generator.random_string()),
            last_name=kwargs.get("last_name", Generator.random_string()),
        )
        user.set_password(kwargs.get("asd", f"pw{random.randint(10000, 999909)}"), )
        # user.user_permissions.set(user_permissions) # have to programm the rights manualy since the test database is always fresh
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
        sender = Generator.generate_customer()
        transfer = BankTransfer(
            iban_from=kwargs.get("iban_from", Generator.generate_account(account_owned_by=sender)),
            iban_to=kwargs.get("iban_to", Generator.generate_account()),
            amount=13,
            created_by=kwargs.get("created_by", sender),
            use_case=Generator.random_string()
        )
        transfer.save()
        return transfer



class SetupClass(TestCase):
    admin_username = 'admin'
    admin_pwd = ':L:3M3pFK"N$Y!Qj'

    bank_customer_username = "USER"
    bank_customer_pwd = "@123456789"

    def create_bank_customer_user(self):
        # user erstellen
        user = User.objects.create(
            username=self.bank_customer_username,

            first_name=f"vorname{random.randint(100000, 999999)}",
            last_name=f"nachname{random.randint(100000, 999999)}",
        )
        user.set_password(self.bank_customer_pwd)
        user.save()
        customer = Generator.generate_customer(
            user=user,
            adress=f"{random.randint(1, 100)}te Straße, {random.randint(1, 234)}"
        )
        customer.save()
        # gruppe
        codenames = [
            'view_banktransfer',
            'add_banktransfer',
            'view_bankaccount',
            'view_bankcustomer',
            'change_bankcustomer',
        ]
        permissions = Permission.objects.filter(codename__in=codenames).all()
        user.user_permissions.set(permissions)
        user.save()
        # customer

        account = Generator.generate_account(account_owned_by=customer, name="Testkonto")
        return account

    def create_superuser(self):
        u = User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_pwd,
        )
        u.save()

    def setUp(self):
        self.create_superuser()
        self.create_bank_customer_user()


class TestApiClass(SetupClass):
    def test_bankaccount(self):
        client = APIClient()
        client.login(username=self.bank_customer_username, password=self.bank_customer_pwd)

        bankuser = User.objects.get(username=self.bank_customer_username).bank_customer

        account = Generator.generate_account(account_owned_by=bankuser)

        # testing accounts
        # List
        # gibt nur eigene Accounts wieder (funktioniert das mit mehereren Accounts?)
        r = client.get(f'/bank/api/bank-accounts/{account.iban}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("iban"), account.iban)

        # Create
        data = {
            "name": "HOLZKOPF",
            "balance": "0.0000",
            "account_owned_by": bankuser.pk
        }
        r = client.post('/bank/api/bank-accounts/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Read not own account

        account_id = Generator.generate_account().iban
        r = client.get('/bank/api/bank-accounts/{}/'.format(account_id))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(r.json().get("name"), data.get("name"))
        # self.assertEqual(r.json().get("balance"), data.get("balance"))
        # self.assertEqual(r.json().get("account_owned_by"), data.get("account_owned_by"))

        # Update
        data = {
            "name": Generator.random_string(),
            "balance": "1.0000",
        }
        r = client.patch(
            '/bank/api/bank-accounts/{}/'.format(account_id),
            data=data,
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(r.json().get("name"), data.get("name"))
        # self.assertEqual(r.json().get("balance"), data.get("balance"))

        # Delete
        r = client.delete('/bank/api/bank-accounts/{}/'.format(account_id))
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_customers(self):
        client = APIClient()
        client.login(username=self.bank_customer_username, password=self.bank_customer_pwd)

        bankuser = User.objects.get(username=self.bank_customer_username).bank_customer

        # testing Customers
        # List
        r = client.get('/bank/api/bank-customers/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # customer = Generator.generate_customer(user=user)
        # Create
        newuser = Generator.generate_user()
        # print(newuser.id)
        data = {
            "adress": Generator.random_string(),
            "user_id": newuser.id
        }
        r = client.post('/bank/api/bank-customers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # BankCustomer erzeugen für newuser
        # Read own
        r = client.get('/bank/api/bank-customers/{}/'.format(bankuser.id))

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("adress"), bankuser.adress)

        # Read other
        otheruser = Generator.generate_customer()
        r = client.get('/bank/api/bank-customers/{}/'.format(otheruser.pk))

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

        # Update
        data = {
            "adress": Generator.random_string(),
        }
        r = client.patch(
            '/bank/api/bank-customers/{}/'.format(bankuser.id),
            data=data,
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("adress"), data.get("adress"))

        # Delete
        r = client.delete('/bank/api/bank-customers/{}/'.format(bankuser.id))
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_transfers(self):
        client = APIClient()
        client.login(username=self.bank_customer_username, password=self.bank_customer_pwd)
        # testing transfers
        user = User.objects.get(username=self.bank_customer_username)
        account_1 = user.bank_customer.account_owned_by.first()  # der account muss mit der ralation auf den eingeloggten user gesetzt werden
        account_2 = Generator.generate_account()
        account_3 = Generator.generate_account()
        transfer = Generator.generate_transfer(
            iban_from=account_1,
            iban_to=account_2,
            amount=15,
            created_by=user.bank_customer
        )

        # List
        r = client.get('/bank/api/bank-transfers/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # get self
        r = client.get(f'/bank/api/bank-transfers/{transfer.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # get other
        other_transfer = Generator.generate_transfer()
        r = client.get(f'/bank/api/bank-transfers/{other_transfer.pk}/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

        # Create
        data = {
            "iban_from": account_1.iban,
            "iban_to": account_2.iban,
            "amount": '20.0000',
            "use_case": Generator.random_string(),
            "created_by": account_1.account_owned_by.pk,
        }
        r = client.post('/bank/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        transfer_id = r.json().get('id')

        # Read
        r = client.get('/bank/api/bank-transfers/{}/'.format(transfer_id))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("iban_from"), account_1.iban)
        self.assertEqual(r.json().get("iban_to"), account_2.iban)
        self.assertEqual(r.json().get("amount"), data.get("amount"))
        self.assertEqual(r.json().get("created_by"), data.get("created_by"))
        self.assertEqual(r.json().get("use_case"), data.get("use_case"))
        # self.assertEqual(r.json().get("is_open"), data.get("is_open"))
        # self.assertEqual(r.json().get("is_success"), data.get("is_success"))
        #

        # Create transfer with different Owner as Sender
        # will create with logged in user as creator
        data = {
            "iban_from": account_1.iban,
            "iban_to": account_3.iban,
            "created_by": account_3.account_owned_by.pk,
            "use_case": Generator.random_string(),
            "amount": '300',
        }
        r = client.post('/bank/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get('created_by'), user.bank_customer.pk)
        # Create transfer from foreign Account
        data = {
            "iban_from": account_2.iban,
            "iban_to": account_3.iban,
            "created_by": account_1.account_owned_by.pk,
            "use_case": Generator.random_string(),
            "amount": '300',
        }
        r = client.post('/bank/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        # Create transfer with no amount set
        data = {
            "iban_from": account_2.iban,
            "iban_to": account_3.iban,
            "created_by": account_3.account_owned_by.pk,
            "use_case": Generator.random_string(),
            "amount": '',
        }
        r = client.post('/bank/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        # transfer mit ungültigem zielkonto IBAN nach Vorgaben
        data = {
            "iban_from": account_2.iban,
            "iban_to": "UNGÜLTIGE EINGABE",
            "created_by": account_3.account_owned_by.pk,
            "use_case": Generator.random_string(),
            "amount": '12',
        }
        r = client.post('/bank/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


        # transfer mit ungültigem Geldbbetrag "z.B. sdtfsgf"
        data = {
            "iban_from": account_2.iban,
            "iban_to": account_3.iban,
            "created_by": account_3.account_owned_by.pk,
            "use_case": Generator.random_string(),
            "amount": 'asd',
        }
        r = client.post('/bank/api/bank-transfers/', data=data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


        # Update
        data = {
            "is_open": False,
            "is_success": True,
        }
        r = client.patch(
            '/bank/api/bank-transfers/{}/'.format(transfer_id),
            data=data,
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #self.assertEqual(r.json().get("is_open"), data.get("is_open"))
        #self.assertEqual(r.json().get("is_success"), data.get("is_success"))
        # wäre es sinnvoll, wenn man self.assertEqual(None,data.get("is_open")) benutzt zum doppelcheck?

        # Delete
        r = client.delete('/bank/api/bank-accounts/{}/'.format(transfer_id))
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
