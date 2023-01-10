from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Client, ClientTag, ClientNetworkCode


class CreateClientTest(APITestCase):
    def test_create_client(self):
        url = reverse('client-list')
        data = {
            "phone_number": "749977777",
            "network_code": 499,
            "tags": ["urgent", "important"],
            "timezone": "UTC"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(ClientTag.objects.count(), 2)
        self.assertEqual(ClientNetworkCode.objects.count(), 1)
        self.assertDictEqual(ClientTag.objects.values()[0], {"id": 1, "tag": "urgent"})
        self.assertDictEqual(ClientNetworkCode.objects.values()[0], {"id": 1, "code": 499})


class DeleteUpdateClientTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        tag = ClientTag.objects.create(tag="urgent")
        code = ClientNetworkCode.objects.create(code=499)
        client = Client.objects.create(phone_number="749977777", network_code=code)
        client.tags.set([tag])

    def test_update_put_client(self):
        url = reverse('client-detail', kwargs={'pk': 1})
        data1 = {
            "timezone": "Europe/Moscow"
        }
        response1 = self.client.put(url, data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

        data2 = {
            "phone_number": "7499123",
            "network_code": 495,
            "tags": ["unimportant"],
            "timezone": "Europe/Moscow"
        }
        response2 = self.client.put(url, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['phone_number'], data2['phone_number'])
        self.assertEqual(response2.data['network_code'], data2['network_code'])
        self.assertEqual(response2.data['tags'], data2['tags'])

    def test_update_patch_client(self):
        url = reverse('client-detail', kwargs={'pk': 1})
        data = {"timezone": "Europe/London"}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["timezone"], data["timezone"])

    def test_delete_client(self):
        url = reverse('client-detail', kwargs={'pk': 1})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)
