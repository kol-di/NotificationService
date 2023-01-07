from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Mailing(models.Model):
    start_datetime = models.DateTimeField(blank=False)
    end_datetime = models.DateTimeField(
        blank=False,
        validators=[MinValueValidator(limit_value=timezone.now)])
    text = models.TextField()
    network_code = models.ManyToManyField(
        'ClientManagement.ClientNetworkCode',
        blank=True)
    client_tags = models.ManyToManyField(
        'ClientManagement.ClientTag',
        blank=True)


class Message(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        blank=False,
        null=False,
        unique=True
    )
    celery_task = models.CharField(
        max_length=50,
        unique=True,
        blank=False)

    PENDING = 'PD'
    STARTED = 'ST'
    SUCCESS = 'SC'
    FAILURE = 'FL'
    RETRY = 'RT'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (STARTED, 'Started'),
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure'),
        (RETRY, 'Retry'),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PENDING)

    mailing = models.ForeignKey(
        Mailing,
        blank=False,
        on_delete=models.CASCADE)
    client = models.ForeignKey(
        'ClientManagement.Client',
        on_delete=models.PROTECT)
    creation_time = models.DateTimeField(
        blank=False)
