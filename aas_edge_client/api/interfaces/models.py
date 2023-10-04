from django.db import models

class Interface(models.Model):
    IPv4Address = models.GenericIPAddressField(protocol='IPv4')
    IPv4SubnetMask = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    Name = models.CharField(max_length=255,null=True, blank=True)
    LinkSpeedReceiveTransmit = models.CharField(max_length=255, null=True, blank=True)
    IPv4DNSServers = models.CharField(max_length=255, null=True, blank=True)
    PrimaryDNSSuffix = models.CharField(max_length=255, null=True, blank=True)
    interface_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.Name
