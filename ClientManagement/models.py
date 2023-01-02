from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

import pytz


class ClientNetworkCode(models.Model):
    code = models.IntegerField(
        validators=[MinValueValidator(limit_value=1)],
        unique=True)

    def __str__(self):
        return str(self.code)


class ClientTag(models.Model):
    tag = models.CharField(
        max_length=150,
        unique=True)

    def __str__(self):
        return self.tag


class Client(models.Model):
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^7.*',
            message='Enter the number in the format 7XXXXXXXXXX')],
        unique=True)
    network_code = models.ForeignKey(
        ClientNetworkCode,
        on_delete=models.PROTECT)
    tags = models.ManyToManyField(
        ClientTag,
        blank=True)

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default='Europe/Moscow')


class Message(models.Model):
    CREATED = 'CR'
    SENT = 'ST'
    RECEIVED = 'RC'
    FAILED = 'FL'
    STATUS_CHOICES = [
        (CREATED, 'Created'),
        (SENT, 'Sent'),
        (RECEIVED, 'Received'),
        (FAILED, 'Failed')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=CREATED)
    creation_time = models.DateTimeField(
        blank=True,
        null=True)
    mailing_id = models.ForeignKey(
        'Mailing.Mailing',
        on_delete=models.PROTECT)
    client_id = models.ForeignKey(
        Client,
        on_delete=models.PROTECT)
