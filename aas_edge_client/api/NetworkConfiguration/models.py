from django.db import models

class Interface(models.Model): 
    STATIC = 'Static'
    AUTOMATIC_DHCP = 'Automatic/DHCP'

    ADDRESS_MODE_CHOICES = [
        (STATIC, 'Static'),
        (AUTOMATIC_DHCP, 'Automatic/DHCP')
    ]

    network_setting = models.ForeignKey('NetworkSetting', on_delete=models.CASCADE, related_name='interfaces')

    IPv4Address = models.GenericIPAddressField(null=True, blank=True)
    IPv4SubnetMask = models.GenericIPAddressField(null=True, blank=True)
    IPv4StandardGateway = models.GenericIPAddressField(null=True, blank=True)
    Name = models.CharField(max_length=255)
    AddressMode = models.CharField(max_length=255, choices=ADDRESS_MODE_CHOICES, null=True, blank=True)
    LinkSpeedReceiveTransmit = models.CharField(max_length=255, null=True, blank=True)
    IPv4DNSServers = models.GenericIPAddressField(null=True, blank=True)
    PrimaryDNSSuffix = models.CharField(max_length=255, null=True, blank=True)

class NetworkSetting(models.Model):
    pass  # No changes needed. The relationship to Interface is managed in the Interface model.

class NetworkConfiguration(models.Model):
    NetworkSetting = models.OneToOneField(NetworkSetting, on_delete=models.CASCADE)
    LastUpdate = models.DateTimeField(null=True, blank=True)
