from rest_framework import serializers
from .models import *
import logging

logger = logging.getLogger(__name__)


class NetAdapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetAdapter
        # fields = ['net_adapter_device', 'net_adapter_status', 'net_adapter_mtu', 'net_adapter_speed',
        #           'net_adapter_duplex', 'net_adapter_bytes_send', 'net_adapter_bytes_recv', 'net_adapter_errs_in',
        #           'net_adapter_drops_in', 'net_adapter_errs_out', 'net_adapter_drops_out', 'MAC', 'IPv4', 'IPv6']
        exclude = ['client']


class DisksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disks
        # fields = ['device', 'total', 'used', 'free', 'fstype', 'mountpoint']
        exclude = ['client']


class ClientSerializer(serializers.ModelSerializer):
    disk = DisksSerializer(many=True)
    adapter = NetAdapterSerializer(many=True)

    def create(self, validated_data):
        disks_data = validated_data.pop('disk')
        net_adapter_data = validated_data.pop('adapter')
        # print(validated_data['name'])
        client = Client.objects.create(**validated_data)

        for disk_data in disks_data:
            Disks.objects.create(client=client, **disk_data)

        for adapter_data in net_adapter_data:
            NetAdapter.objects.create(client=client, **adapter_data)
        return client

    def update(self, instance, validated_data):
        disks_data = validated_data.pop('disk')
        net_adapter_data = validated_data.pop('adapter')
        instance = super().update(instance, validated_data)
        instance.disk.all().delete()
        instance.adapter.all().delete()

        for disks_data in disks_data:
            Disks.objects.update_or_create(client=instance, **disks_data)
        for adapter_data in net_adapter_data:
            NetAdapter.objects.update_or_create(client=instance, **adapter_data)

        return instance
    class Meta:
        model = Client
        fields = '__all__'
