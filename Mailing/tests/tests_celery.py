from ClientManagement.models import Client, ClientTag, ClientNetworkCode
from Mailing.models import Message

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.utils import timezone


class CeleryMessageTest(APITestCase):
    def setUp(self):
        """
        Client 1; 495, [important]
        Client 2; 499, [unimportant]
        Client 3; 495, [important]
        """
        tags = [ClientTag(tag=tag) for tag in ['important', 'unimportant']]
        ClientTag.objects.bulk_create(tags)
        codes = [ClientNetworkCode(code=code) for code in [495, 499]]
        ClientNetworkCode.objects.bulk_create(codes)
        clients = Client.objects.bulk_create([
            Client(phone_number=74991, network_code=codes[1]),
            Client(phone_number=74951, network_code=codes[0]),
            Client(phone_number=74992, network_code=codes[1])
        ])
        clients[0].tags.set([tags[0]])
        clients[1].tags.set([tags[1]])
        clients[2].tags.set([tags[0]])

    def test_send_celery_code_match(self):
        url = reverse('mailing-list')
        data = {
            "start_datetime": str(timezone.now() - timezone.timedelta(days=2)),
            "end_datetime": str(timezone.now() + timezone.timedelta(days=2)),
            "text": "TEXT_CELERY_CODE_MATCH",
            "network_code": [
                495
            ]
        }
        self.client.post(url, data, format='json')
        self.assertEqual(Message.objects.count(), 1)

    def test_celery_tag_match(self):
        url = reverse('mailing-list')
        data = {
            "start_datetime": str(timezone.now() - timezone.timedelta(days=2)),
            "end_datetime": str(timezone.now() + timezone.timedelta(days=2)),
            "text": "TEXT_CELERY_TAG_MATCH",
            "client_tags": [
                "important"
            ]
        }
        self.client.post(url, data, format='json')
        self.assertEqual(Message.objects.count(), 2)
