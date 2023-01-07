from .models import Mailing, Message
from ClientManagement.models import ClientTag, ClientNetworkCode

from rest_framework import serializers


class MailingSerializer(serializers.ModelSerializer):
    client_tags = serializers.SlugRelatedField(
        slug_field='tag',
        many=True,
        allow_null=True,
        queryset=ClientTag.objects.all(),
        required=False)
    network_code = serializers.SlugRelatedField(
        slug_field='code',
        allow_null=True,
        many=True,
        queryset=ClientNetworkCode.objects.all(),
        required=False)

    class Meta:
        model = Mailing
        fields = ('id', 'start_datetime', 'end_datetime', 'text', 'network_code', 'client_tags')

    def validate(self, attrs):
        if attrs['start_datetime'] >= attrs['end_datetime']:
            raise serializers.ValidationError("End datetime should be less than start")
        return attrs


class MessageSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(read_only=True, source='client')

    class Meta:
        model = Message
        fields = ['id', 'status', 'client_id', 'creation_time']


class MailingMessagesStatsSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Mailing
        fields = ['id', 'text', 'messages']
