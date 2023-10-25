from rest_framework import serializers
from .models import Interface, NetworkSetting, NetworkConfiguration

class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = [
            'IPv4Address', 
            'IPv4SubnetMask',
            'IPv4StandardGateway',
            'Name', 
            'AddressMode',
            'LinkSpeedReceiveTransmit', 
            'IPv4DNSServers', 
            'PrimaryDNSSuffix',
        ]

class NetworkSettingSerializer(serializers.ModelSerializer):
    interfaces = InterfaceSerializer(many=True)

    class Meta:
        model = NetworkSetting
        fields = ['interfaces']

    def create(self, validated_data):
        interfaces_data = validated_data.pop('interfaces')
        network_setting = NetworkSetting.objects.create(**validated_data)

        for interface_data in interfaces_data:
            Interface.objects.create(network_setting=network_setting, **interface_data)
        
        return network_setting

    def update(self, instance, validated_data):
        interfaces_data = validated_data.pop('interfaces')
        
        # Remove and recreate interfaces (you can optimize this for better performance)
        instance.interfaces.all().delete()

        for interface_data in interfaces_data:
            Interface.objects.create(network_setting=instance, **interface_data)

        return instance

class NetworkConfigurationSerializer(serializers.ModelSerializer):
    NetworkSetting = NetworkSettingSerializer()

    class Meta:
        model = NetworkConfiguration
        fields = ['NetworkSetting', 'LastUpdate']

    def create(self, validated_data):
        network_setting_data = validated_data.pop('NetworkSetting')
        network_setting_serializer = NetworkSettingSerializer(data=network_setting_data)

        if network_setting_serializer.is_valid(raise_exception=True):
            network_setting = network_setting_serializer.save()

        network_configuration = NetworkConfiguration.objects.create(NetworkSetting=network_setting, **validated_data)
        return network_configuration

    def update(self, instance, validated_data):
        network_setting_data = validated_data.pop('NetworkSetting')
        network_setting_serializer = NetworkSettingSerializer(instance.NetworkSetting, data=network_setting_data)

        if network_setting_serializer.is_valid(raise_exception=True):
            network_setting_serializer.save()

        return super().update(instance, validated_data)
