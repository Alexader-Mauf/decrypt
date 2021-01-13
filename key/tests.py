from django.test import TestCase

# Create your tests here.
class TestAPIEndpointAuthorization(TestCase):
    def test_api_authorization(self):
        urls = [
            'salechannels',
            'offers',
            'exporters',
            'knowledge-items',
            'offer-ext-status',
            'offer-status',
        ]
        client = APIClient()
        for x in urls:
            r = client.get('/marketplace/api/{}/'.format(x))
            self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


class APIKnowledgeItemTestCase(core_tests.SetupClass):
    def test_knowledge(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)

        response = client.post(
            'http://0.0.0.0:8000/marketplace/api/knowledge-items/import/',
            data={
                "salechannel": "otto-market-tp-de",
                "group": "BRAND",
                "value": "My Bento"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        item_id = response.json().get('results', {}).get('id')
        self.assertIsNotNone(item_id)

        response = client.get(
            'http://0.0.0.0:8000/marketplace/api/knowledge-items/{}/'.format(item_id),
            format='json'
        )
        self.assertEqual(response.status_code, 200)

        response = client.get(
            'http://0.0.0.0:8000/marketplace/api/knowledge-items/',
            format='json'
        )
        self.assertEqual(response.status_code, 200)