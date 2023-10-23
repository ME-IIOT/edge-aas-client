from rest_framework import serializers
from .models import Processor, Memory, Hardware, SystemInformation

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = [
            'CpuType', 
            'CpuCores',
            'CpuClock',
            'CpuUsage', 
            'CpuTemperature',
        ]

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = [
            'RAMInstalled', 
            'RAMFree',
            'DiskInstalled',
            'DiskFree', 
        ]

class HardwareSerializer(serializers.ModelSerializer):
    Processor = ProcessorSerializer()
    Memory = MemorySerializer()

    class Meta:
        model = Hardware
        fields = [
            'Processor', 
            'Memory',
            'BoardTemperature',
        ]
    
    def create(self, validated_data):
        processor_data = validated_data.pop('Processor')
        memory_data = validated_data.pop('Memory')

        processor = ProcessorSerializer.create(ProcessorSerializer(), validated_data=processor_data)
        memory = MemorySerializer.create(MemorySerializer(), validated_data=memory_data)

        hardware = Hardware.objects.create(Processor=processor, Memory=memory, **validated_data)
        return hardware
    
    def update(self, instance, validated_data):
        # Update nested Processor and Memory instances
        self._update_processor(instance.Processor, validated_data.pop('Processor'))
        self._update_memory(instance.Memory, validated_data.pop('Memory'))
        
        # Update scalar fields
        return super().update(instance, validated_data)
    
    def _update_processor(self, processor_instance, processor_data):
        serializer = ProcessorSerializer(instance=processor_instance, data=processor_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    def _update_memory(self, memory_instance, memory_data):
        serializer = MemorySerializer(instance=memory_instance, data=memory_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

class SystemInformationSerializer(serializers.ModelSerializer):
    Hardware = HardwareSerializer()
    LastUpdate = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%SZ'])
    
    class Meta:
        model = SystemInformation
        fields = ['Hardware', 'HealthStatus', 'LastUpdate']

    def create(self, validated_data):
        hardware_data = validated_data.pop('Hardware')
        hardware = HardwareSerializer.create(HardwareSerializer(), validated_data=hardware_data)
        
        # Create SystemInformation object
        system_information = SystemInformation.objects.create(Hardware=hardware, **validated_data)
        
        return system_information

    def update(self, instance, validated_data):
        # Update nested Hardware instance
        self._update_hardware(instance.Hardware, validated_data.pop('Hardware'))
        
        # Update scalar fields
        return super().update(instance, validated_data)
    
    def _update_hardware(self, hardware_instance, hardware_data):
        serializer = HardwareSerializer(instance=hardware_instance, data=hardware_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


