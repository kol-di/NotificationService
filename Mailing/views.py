from .models import Mailing, Message
from .serializers import MailingSerializer, MailingMessagesStatsSerializer
from .tasks import process_mailing

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .celery import app


class MailingViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get information about particular mailing.

    list:
    Get information about all mailings.

    create:
    Create new mailing and schedule related messages.

    destroy:
    Delete existing mailing and retrieve related messages.

    update:
    Update mailing parameters and reschedule related messages.
    Required fields must be specified.

    partial_update:
    Update mailing parameters and reschedule related messages.
    Required fields will be derived from older version if not specified.
    """
    serializer_class = MailingSerializer

    def get_queryset(self):
        return Mailing.objects.all()

    def perform_update(self, serializer):
        if serializer.instance is not None:
            self.perform_destroy(serializer.instance)
        instance = serializer.save()
        process_mailing(instance)

    def perform_create(self, serializer):
        instance = serializer.save()
        process_mailing(instance)

    def perform_destroy(self, instance):
        app.control.revoke(list(instance.message_set.values_list('celery_task', flat=True)), terminate=True)
        instance.delete()

    @action(
        methods=['get'],
        detail=True,
        serializer_class=MailingMessagesStatsSerializer)
    def stats(self, request, pk=None):
        """
        Get information about messages, related to the given mailing
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=False,
        url_path='stats')
    def mailing_stats(self, request, pk=None):
        """
        Get aggregated statistics about all messages and their statuses
        """
        queryset = self.get_queryset().prefetch_related('message_set')

        res = []
        for mail in queryset:
            res.append({
                'Mail ID': mail.id,
                'Mail Text': mail.text,
                'Msg Success': mail.message_set.filter(status=Message.SUCCESS).count(),
                'Msg Pending': mail.message_set.filter(status=Message.PENDING).count(),
                'Msg Failure': mail.message_set.filter(status=Message.FAILURE).count()
            })

        return Response(res)
