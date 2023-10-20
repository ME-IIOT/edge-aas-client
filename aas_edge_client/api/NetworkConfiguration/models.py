from django.db import models


class Interface(models.Model): 
    STATIC = 'Static'
    AUTOMATIC_DHCP = 'Automatic/DHCP'

    ADDRESS_MODUS_CHOICES = [
        (STATIC, 'Static'),
        (AUTOMATIC_DHCP, 'Automatic/DHCP')
    ]

    IPv4Address = models.GenericIPAddressField( null=True, blank=True)
    IPv4SubnetMask = models.GenericIPAddressField( null=True, blank=True)
    IPv4StandardGateway= models.GenericIPAddressField( null=True, blank=True)
    Name = models.CharField(max_length=255, null=True, blank=True)
    AddressMode = models.CharField( max_length=255, choices=ADDRESS_MODUS_CHOICES, null=True, blank=True)
    LinkSpeedReceiveTransmit = models.CharField(max_length=255, null=True, blank=True)
    IPv4DNSServers = models.GenericIPAddressField( null=True, blank=True)
    PrimaryDNSSuffix = models.CharField(max_length=255, null=True, blank=True)


class NetworkSetting(models.Model):
    InterfaceEth0 = models.OneToOneField(
        Interface, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='interfaceEth0'
    )
    InterfaceEth1 = models.OneToOneField(
        Interface, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='interfaceEth1'
    )


class NetworkConfiguration(models.Model):
    NetworkSetting = models.OneToOneField(
        NetworkSetting, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    LastUpdate = models.DateTimeField(null=True, blank=True)