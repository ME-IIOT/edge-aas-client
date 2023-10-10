from rest_framework import serializers
from .models import TemperatureElements, Temperature, Sensors

class TemperatureElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureElements
        fields = [
            'Time', 
            'Value',
        ]

class TemperatureSerializer(serializers.ModelSerializer):
    Temperature = TemperatureElementsSerializer()

    class Meta:
        model = Temperature
        fields = [
            'Temperature',
        ]
    
    def create(self, validated_data):
        temperature_elements_data = validated_data.pop('Temperature')
        temperature_elements = TemperatureElements.objects.create(**temperature_elements_data)
        # temperature = Temperature.objects.create(temperature=temperature_elements, **validated_data)
        temperature = Temperature.objects.create(Temperature=temperature_elements, **validated_data)
        return temperature
    
    def update(self, instance, validated_data):
        temperature_elements_data = validated_data.pop('Temperature')
        self._update_temperature_elements(instance.Temperature, temperature_elements_data)
        return super().update(instance, validated_data)
    
    def _update_temperature_elements(self, element_instance, element_data):
        serializer = TemperatureElementsSerializer(instance=element_instance, data=element_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

class SensorsSerializer(serializers.ModelSerializer):
    Sensors = TemperatureSerializer()

    class Meta:
        model = Sensors
        fields = [
            'Sensors',
        ]
    
    def create(self, validated_data):
        temperature_data = validated_data.pop('Sensors')
        temperature = TemperatureSerializer().create(temperature_data)
        sensor = Sensors.objects.create(Sensors=temperature, **validated_data)
        return sensor
    
    def update(self, instance, validated_data):
        temperature_data = validated_data.pop('Sensors')
        self._update_temperature(instance.Sensors, temperature_data)
        return super().update(instance, validated_data)
    
    def _update_temperature(self, temperature_instance, temperature_data):
        serializer = TemperatureSerializer(instance=temperature_instance, data=temperature_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
