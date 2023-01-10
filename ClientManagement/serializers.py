from .models import Client, ClientTag, ClientNetworkCode

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.get_queryset().create(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')


class ClientSerializer(serializers.ModelSerializer):
    tags = CreatableSlugRelatedField(
        slug_field='tag',
        many=True,
        allow_null=True,
        queryset=ClientTag.objects.all(),
        required=False)
    network_code = CreatableSlugRelatedField(
        slug_field='code',
        queryset=ClientNetworkCode.objects.all())

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'network_code', 'tags', 'timezone',)




