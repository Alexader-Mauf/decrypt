from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate

from django.contrib.auth.models import User


# Create your tests here.
class TestAPIEndpointAuthorization(TestCase):
    def test_api_authorization(self):
        urls = [
            'bank_customers',
            'bank_accounts',
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


class TestAPIFunctionality(SetupClass):
    def test_api_post(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)
        # mache eine überweisung
        response = client.post(
            '/bank/api/bank_accounts/',
            data={
                "to_acc": "IBAN",
                "amount":"123,21",
                "from_acc":"IBAN",

            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)


        self.assertEqual(response.status_code, 200)

        # sucht nach einem konto
        item_id = response.json().get('to_acc')
        response = client.get(
            '/bank/api/bank_accounts/{}/'.format(item_id),
            format='json'
        )

        self.assertIsNotNone(item_id)
        self.assertEqual(response.status_code, 200)

        # sucht nach nichtexistentem Konto
        item_id = "asdasdasdf"
        response = client.get(
            '/bank/api/bank_accounts/{}/'.format(item_id),
            format='json'
        )


        self.assertEqual(response.status_code, 404)

