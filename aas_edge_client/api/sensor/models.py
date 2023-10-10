from django.db import models

class TemperatureElements(models.Model):
    Time = models.CharField(max_length=255,null=True, blank=True)
    Value = models.FloatField()

class Temperature(models.Model):
    Temperature = models.OneToOneField(
        TemperatureElements, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='Temperature'
    )

class Sensors(models.Model):
    Sensors = models.OneToOneField(
        Temperature, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
    )