from rest_framework import serializers
from .models import Interface, NetworkSetting, NetworkConfiguration

class InterfaceSerializer(serializers.ModelSerializer):
    IPv4DNSServers = serializers.IPAddressField(required=False, allow_blank=True)
    IPv4StandardGateway = serializers.IPAddressField(required=False, allow_blank=True)
    IPv4SubnetMask = serializers.IPAddressField(required=False, allow_blank=True)
    IPv4Address = serializers.IPAddressField(required=False, allow_blank=True)

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
    InterfaceEth0 = InterfaceSerializer()
    InterfaceEth1 = InterfaceSerializer()

    class Meta:
        model = NetworkSetting
        fields = [
            'InterfaceEth0', 
            'InterfaceEth1',
        ]
    
    def create(self, validated_data):
        interfaceEth0_data = validated_data.pop('InterfaceEth0')
        interfaceEth1_data = validated_data.pop('InterfaceEth1')

        interfaceEth0 = InterfaceSerializer.create(InterfaceSerializer(), validated_data=interfaceEth0_data)
        interfaceEth1 = InterfaceSerializer.create(InterfaceSerializer(), validated_data=interfaceEth1_data)

        network_setting = NetworkSetting.objects.create(InterfaceEth0=interfaceEth0, InterfaceEth1=interfaceEth1, **validated_data)
        return network_setting
    
    def update(self, instance, validated_data):
        # Update nested Interface instances
        self._update_interface(instance.InterfaceEth0, validated_data.pop('InterfaceEth0'))
        self._update_interface(instance.InterfaceEth1, validated_data.pop('InterfaceEth1'))
        
        # Update scalar fields
        return super().update(instance, validated_data)
    
    def _update_interface(self, interface_instance, interface_data):
        serializer = InterfaceSerializer(instance=interface_instance, data=interface_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


class NetworkConfigurationSerializer(serializers.ModelSerializer):
    NetworkSetting = NetworkSettingSerializer()  # Reusing the NetworkSettingSerializer you provided
    LastUpdate = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%SZ'])

    class Meta:
        model = NetworkConfiguration
        fields = ['NetworkSetting', 'LastUpdate']

    def create(self, validated_data):
        network_setting_data = validated_data.pop('NetworkSetting')
        network_setting = NetworkSettingSerializer.create(NetworkSettingSerializer(), validated_data=network_setting_data)
        
        # Create NetworkConfiguration object
        network_configuration = NetworkConfiguration.objects.create(NetworkSetting=network_setting, **validated_data)
        
        return network_configuration

    def update(self, instance, validated_data):
        # Update nested NetworkSetting instance
        self._update_network_setting(instance.NetworkSetting, validated_data.pop('NetworkSetting'))
        
        # Update scalar fields
        return super().update(instance, validated_data)

    def _update_network_setting(self, network_setting_instance, network_setting_data):
        serializer = NetworkSettingSerializer(instance=network_setting_instance, data=network_setting_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()