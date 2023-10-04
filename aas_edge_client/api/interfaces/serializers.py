from rest_framework import serializers
from .models import InterfaceElements, Interface, NetworkSetting

class InterfaceElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceElements
        fields = [
            'Name', 
            'IPv4Address', 
            'IPv4SubnetMask', 
            'LinkSpeedReceiveTransmit', 
            'IPv4DNSServers', 
            'PrimaryDNSSuffix',
        ]

class InterfaceSerializer(serializers.ModelSerializer):
    InterfaceEth0 = InterfaceElementsSerializer()
    InterfaceEth1 = InterfaceElementsSerializer()

    class Meta:
        model = Interface
        fields = [
            'InterfaceEth0', 
            'InterfaceEth1',
        ]
    def update(self, instance, validated_data):
        # Update nested InterfaceElements instances
        self._update_interface_element(instance.InterfaceEth0, validated_data.pop('InterfaceEth0'))
        self._update_interface_element(instance.InterfaceEth1, validated_data.pop('InterfaceEth1'))
        
        # Update scalar fields
        return super().update(instance, validated_data)

    def _update_interface_element(self, element_instance, element_data):
        serializer = InterfaceElementsSerializer(instance=element_instance, data=element_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

class NetworkSettingSerializer(serializers.ModelSerializer):
    NetworkSetting = InterfaceSerializer()

    class Meta:
        model = NetworkSetting
        fields = [
            'NetworkSetting',
        ]


    def create(self, validated_data):
        interface_data = validated_data.pop('NetworkSetting')
        interface_elements_0 = interface_data.get('InterfaceEth0')
        interface_elements_1 = interface_data.get('InterfaceEth1')
        
        # Create InterfaceElements objects
        interface_element_obj_0 = InterfaceElements.objects.create(**interface_elements_0)
        interface_element_obj_1 = InterfaceElements.objects.create(**interface_elements_1)
        
        # Create Interface object
        interface_data['InterfaceEth0'] = interface_element_obj_0
        interface_data['InterfaceEth1'] = interface_element_obj_1
        interface = Interface.objects.create(**interface_data)
        
        # Create NetworkSetting object
        network_setting = NetworkSetting.objects.create(NetworkSetting=interface, **validated_data)
        
        return network_setting
    
    def update(self, instance, validated_data):
        # Update nested Interface instance
        self._update_interface(instance.NetworkSetting, validated_data.pop('NetworkSetting'))
        
        # Update scalar fields
        return super().update(instance, validated_data)

    def _update_interface(self, interface_instance, interface_data):
        serializer = InterfaceSerializer(instance=interface_instance, data=interface_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()