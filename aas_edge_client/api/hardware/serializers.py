from rest_framework import serializers
from .models import HardwareElements, ProcessorElements, MemoryElements, Hardware

class ProcessorElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessorElements
        fields = [
            'CpuType', 
            'CpuCores',
            'CpuClock',
            'CpuUsage', 
            'CpuTemperature',
        ]

class MemoryElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryElements
        fields = [
            'RAMInstalled', 
            'RAMFree',
            'DiskInstalled',
            'DiskFree', 
        ]

class HardwareElementsSerializer(serializers.ModelSerializer):
    Processor = ProcessorElementsSerializer()
    Memory = MemoryElementsSerializer()

    class Meta:
        model = HardwareElements
        fields = [
            'Processor', 
            'Memory',
            'BoardTemperature',
        ]
    def update(self, instance, validated_data):
        # Update nested ProcessorElements instances
        self._update_processor_element(instance.Processor, validated_data.pop('Processor'))
        # Update nested MemoryElements instances
        self._update_memory_element(instance.Memory, validated_data.pop('Memory'))
        
        # Update scalar fields
        return super().update(instance, validated_data)

    def _update_processor_element(self, element_instance, element_data):
        serializer = ProcessorElementsSerializer(instance=element_instance, data=element_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    def _update_memory_element(self, element_instance, element_data):
        serializer = MemoryElementsSerializer(instance=element_instance, data=element_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

class HardwareSerializers(serializers.ModelSerializer):
    Hardware = HardwareElementsSerializer()

    class Meta:
        model = Hardware
        fields = [
            'Hardware',
        ]

    def create(self, validated_data):
        hardware_data = validated_data.pop('Hardware')
        processor_elements = hardware_data.get('Processor')
        memory_elements = hardware_data.get('Memory')
        
        # Create ProcessorElements objects
        processor_element_obj = ProcessorElements.objects.create(**processor_elements)
        memory_element_obj = MemoryElements.objects.create(**memory_elements)
        
        # Create HardwareElements object
        hardware_data['Processor'] = processor_element_obj
        hardware_data['Memory'] = memory_element_obj
        hardware = HardwareElements.objects.create(**hardware_data)
        
        # Create Hardware object
        hardware = Hardware.objects.create(Hardware=hardware, **validated_data)
        
        return hardware
    
    def update(self, instance, validated_data):
        # Update nested HardwareElements instance
        self._update_hardware(instance.Hardware, validated_data.pop('Hardware'))
        
        # Update scalar fields
        return super().update(instance, validated_data)
    
    def _update_hardware(self, element_instance, element_data):
        serializer = HardwareElementsSerializer(instance=element_instance, data=element_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
