# from ClientManagement.models import ClientTag, ClientNetworkCode

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Mailing(models.Model):
    start_datetime = models.DateTimeField(blank=False)
    end_datetime = models.DateTimeField(
        blank=True,
        null=True,
        validators=[MinValueValidator(limit_value=timezone.now)])
    text = models.TextField()
    network_code = models.ManyToManyField(
        'ClientManagement.ClientNetworkCode',
        blank=True,
        null=True)
    client_tags = models.ManyToManyField(
        'ClientManagement.ClientTag',
        blank=True,
        null=True)
