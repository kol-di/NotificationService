from ClientManagement.models import Client, ClientTag, ClientNetworkCode
from Mailing.models import Mailing

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class CreateMailingTest(APITestCase):
    def setUp(self):
        tags = [ClientTag(tag=tag) for tag in ['important', 'unimportant']]
        ClientTag.objects.bulk_create(tags)
        codes = [ClientNetworkCode(code=code) for code in [495, 499]]
        ClientNetworkCode.objects.bulk_create(codes)
        Client.objects.bulk_create([
            Client(phone_number=74991, network_code=codes[1]),
            Client(phone_number=74951, network_code=codes[0]),
            Client(phone_number=74992, network_code=codes[1])
        ])

    def test_create_mailing(self):
        url = reverse('mailing-list')
        data = {
            "start_datetime": str(timezone.now() - timezone.timedelta(days=1)),
            "end_datetime": str(timezone.now() + timezone.timedelta(days=1)),
            "text": "TEXT",
            "network_code": [
                499
            ],
            "client_tags": [
                "important"
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(parse_datetime(response.data['start_datetime']), parse_datetime(data['start_datetime']))
        self.assertEqual(parse_datetime(response.data['end_datetime']), parse_datetime(data['end_datetime']))
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['client_tags'], data['client_tags'])
        self.assertEqual(response.data['network_code'], data['network_code'])


class DeleteUpdateMailingTest(APITestCase):
    def setUp(self):
        tags = [ClientTag(tag=tag) for tag in ['important', 'unimportant']]
        ClientTag.objects.bulk_create(tags)
        codes = [ClientNetworkCode(code=code) for code in [495, 499]]
        ClientNetworkCode.objects.bulk_create(codes)
        Client.objects.bulk_create([
            Client(phone_number=74991, network_code=codes[1]),
            Client(phone_number=74951, network_code=codes[0]),
            Client(phone_number=74992, network_code=codes[1])
        ])
        mailing = Mailing.objects.create(
            start_datetime=timezone.now() - timezone.timedelta(days=1),
            end_datetime=str(timezone.now() + timezone.timedelta(days=1)),
            text="TEXT")
        mailing.client_tags.set([tags[1]])
        mailing.network_code.set([codes[1]])

    def test_update_put_mailing(self):
        url = reverse('mailing-detail', kwargs={'pk': 1})

        # assert put throws error without required parameters
        data1 = {
            "text": "TEXT_PUT"
        }
        response1 = self.client.put(url, data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

        # assert put normal workflow
        data2 = {
            "start_datetime": str(timezone.now() - timezone.timedelta(days=2)),
            "end_datetime": str(timezone.now() + timezone.timedelta(days=2)),
            "text": "TEXT_PUT",
            "network_code": [
                495
            ],
            "client_tags": [
                "important"
            ]
        }
        response2 = self.client.put(url, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(parse_datetime(response2.data['start_datetime']), parse_datetime(data2['start_datetime']))
        self.assertEqual(parse_datetime(response2.data['end_datetime']), parse_datetime(data2['end_datetime']))
        self.assertEqual(response2.data['text'], data2['text'])
        self.assertEqual(response2.data['network_code'], data2['network_code'])

    def test_update_patch_mailing(self):
        url = reverse('mailing-detail', kwargs={'pk': 1})
        data = {
            "text": "TEXT_PATCH"
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.data['text'], data['text'])

    def test_delete_mailing(self):
        url = reverse('mailing-detail', kwargs={'pk': 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)





