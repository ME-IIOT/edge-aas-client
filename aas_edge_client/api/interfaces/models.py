from django.db import models


class InterfaceElements(models.Model): 
    IPv4Address = models.GenericIPAddressField( null=True, blank=True)
    IPv4SubnetMask = models.GenericIPAddressField( null=True, blank=True)
    IPv4StandardGateway= models.GenericIPAddressField( null=True, blank=True)
    HostName = models.CharField(max_length=255, null=True, blank=True)
    AddressModus = models.CharField( max_length=255, null=True, blank=True)
    LinkSpeedReceiveTransmit = models.CharField(max_length=255, null=True, blank=True)
    IPv4DNSServers = models.GenericIPAddressField( null=True, blank=True)
    PrimaryDNSSuffix = models.CharField(max_length=255, null=True, blank=True)


class Interface(models.Model):
    InterfaceEth0 = models.OneToOneField(
        InterfaceElements, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='interfaceEth0'
    )
    InterfaceEth1 = models.OneToOneField(
        InterfaceElements, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='interfaceEth1'
    )


class NetworkSetting(models.Model):
    NetworkSetting = models.OneToOneField(
        Interface, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )