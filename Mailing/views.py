from .models import Mailing
from .serializers import MailingSerializer

from rest_framework import viewsets


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer

    def get_queryset(self):
        return Mailing.objects.all()
