import time

from celery import shared_task, Task
from django.utils import timezone
import requests
from dotenv import dotenv_values
import json
import uuid
import logging

from ClientManagement.models import Client
from .models import Message


class ExternalHTTPException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code
        self.message = f"External API returned {self.status_code} status code"
        super().__init__(self.message)


class CallbackTask(Task):
    def on_success(self, retval, celery_task_id, args, kwargs):
        logging.info(f'Message id:{args[2]} status changed: {Message.SUCCESS}')
        Message.objects.filter(pk=args[2]).update(status=Message.SUCCESS)

    def on_failure(self, exc, celery_task_id, args, kwargs, einfo):
        logging.info(f'Message id:{args[2]} status changed: {Message.FAILURE}')
        Message.objects.filter(pk=args[2]).update(status=Message.FAILURE)


@shared_task(base=CallbackTask)
def send_message(client_id, text, task_id):
    phone = Client.objects.get(pk=client_id).phone_number

    endpoint = f'https://probe.fbrq.cloud/v1/send/{task_id}'
    headers = {
        "Authorization": "Bearer {}".format(dotenv_values('.env')['JWT_TOKEN'])
    }
    data = {
        "id": task_id,
        "phone": phone,
        "text": text
    }
    res = requests.post(endpoint, data=json.dumps(data), headers=headers)
    if res.status_code >= 300:
        raise ExternalHTTPException(res.status_code)


def choose_client_ids(codes, tags):
    # empty codes list means all codes
    if codes:
        query1 = Client.objects.select_related('network_code').filter(network_code__code__in=codes)
    else:
        query1 = Client.objects.all()

    # empty tags list means all tags
    if tags:
        query2 = query1.prefetch_related('tags').filter(tags__tag__in=tags)
    else:
        query2 = query1

    ids = query2.values_list('pk', flat=True)

    return ids


def process_mailing(mailing_instance):
    codes, tags, text, end_datetime, start_datetime = \
        list(map(lambda x: x[1], mailing_instance.network_code.values_list())), \
        list(map(lambda x: x[1], mailing_instance.client_tags.values_list())), \
        mailing_instance.text, \
        mailing_instance.end_datetime, \
        mailing_instance.start_datetime

    client_ids = choose_client_ids(codes, tags)
    for client_id in client_ids:
        task_id = uuid.uuid1()
        celery_task_id, api_task_id = task_id.hex, task_id.int >> 65

        Message.objects.create(
            pk=api_task_id,
            celery_task=celery_task_id,
            mailing=mailing_instance,
            creation_time=timezone.now(),
            client=Client.objects.get(pk=client_id))
        res = send_message.apply_async(
            (client_id, text, api_task_id),
            expires=end_datetime,
            eta=max(timezone.now(), start_datetime),
            task_id=celery_task_id,
        )
        logging.info(f'Message id:{api_task_id} created')
