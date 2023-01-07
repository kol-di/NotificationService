from .models import Client
from .serializers import ClientSerializer

from rest_framework import viewsets


class ClientViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get information about particular client.

    list:
    Get information about all clients.

    create:
    Create new client.
    New tags and status codes will be also created.

    destroy:
    Delete existing client.
    Related messages will be retrieved.

    update:
    Update client parameters.
    Related messages will persist.
    Required fields must be specified.


    partial_update:
    Update client parameters.
    Related messages will persist.
    Required fields will be derived from older version if not specified.
    """
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.all()
