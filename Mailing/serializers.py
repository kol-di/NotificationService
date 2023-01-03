from .models import Mailing
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
        fields = ('start_datetime', 'end_datetime', 'text', 'network_code', 'client_tags')

    def validate(self, attrs):
        if attrs['start_datetime'] >= attrs['end_datetime']:
            raise serializers.ValidationError("End datetime should be less than start")
        return attrs




