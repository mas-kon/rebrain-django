from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import *
# import logging
#
# logger = logging.getLogger(__name__)


class ClientSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # disks = validated_data.pop('disk')
        # net_adapter = validated_data.pop('adapter')
        try:
            Client.objects.get(name=validated_data['name'])
        except ObjectDoesNotExist:
            client = Client.objects.create(**validated_data)
        finally:
            client = Client.objects.get(name=validated_data['name'])

        return client

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Client
        fields = '__all__'
