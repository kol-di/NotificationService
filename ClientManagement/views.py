from .models import Client
from .serializers import ClientSerializer

from rest_framework import viewsets


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.all()
