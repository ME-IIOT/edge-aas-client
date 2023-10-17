from django.db import models

# Create your models here.

class Processor(models.Model):
    CpuType = models.CharField(max_length=255, null=True, blank=True)
    CpuCores = models.CharField(max_length=255, null=True, blank=True)
    CpuClock = models.CharField(max_length=255, null=True, blank=True)
    CpuUsage = models.CharField(max_length=255, null=True, blank=True)
    CpuTemperature = models.CharField(max_length=255, null=True, blank=True)

class Memory(models.Model):
    RAMInstalled = models.CharField(max_length=255, null=True, blank=True)
    RAMFree = models.CharField(max_length=255, null=True, blank=True)
    DiskInstalled = models.CharField(max_length=255, null=True, blank=True)
    DiskFree = models.CharField(max_length=255, null=True, blank=True)

class Hardware(models.Model):
    Processor = models.OneToOneField(
        Processor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    Memory = models.OneToOneField(
        Memory, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    BoardTemperature = models.CharField(max_length=255, null=True, blank=True)

class SystemInformation(models.Model):
    Hardware = models.OneToOneField(
        Hardware, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    HealthStatus = models.CharField(max_length=255, null=True, blank=True)
    LastUpdate = models.DateTimeField(null=True, blank=True)