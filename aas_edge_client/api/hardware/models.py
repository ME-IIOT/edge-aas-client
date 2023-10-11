from django.db import models

# Create your models here.

class ProcessorElements(models.Model):
    CpuType = models.CharField(max_length=255, null=True, blank=True)
    CpuCores = models.CharField(max_length=255, null=True, blank=True)
    CpuClock = models.CharField(max_length=255, null=True, blank=True)
    CpuUsage = models.CharField(max_length=255, null=True, blank=True)
    CpuTemperature = models.CharField(max_length=255, null=True, blank=True)

class MemoryElements(models.Model):
    RAMInstalled = models.CharField(max_length=255, null=True, blank=True)
    RAMFree = models.CharField(max_length=255, null=True, blank=True)
    DiskInstalled = models.CharField(max_length=255, null=True, blank=True)
    DiskFree = models.CharField(max_length=255, null=True, blank=True)

class HardwareElements(models.Model):
    Processor = models.OneToOneField(
        ProcessorElements, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    Memory = models.OneToOneField(
        MemoryElements, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    BoardTemperature = models.CharField(max_length=255, null=True, blank=True)

class Hardware(models.Model):
    Hardware = models.OneToOneField(
        HardwareElements, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )