from celery import shared_task
from EdgeAasMessageHandler.EdgePollingHandler import (PollingSystemInformationServerHandler,
                                                        PollingNetworkConfigurationServerHandler,
                                                        PollingSystemInformationClientHandler,
                                                        EdgePollingEvent)
# from EdgeAasMessageHandler.Reactor import AsyncReactor
# from EdgeAasMessageHandler.EdgeHandler import Job

from django.conf import settings
import asyncio
# import aiohttp
import requests

# reactor = AsyncReactor()

@shared_task
def aasx_server_polling():
    print("aasx_server_polling")  
    url = f"{settings.CLIENT_URL}/periodic_task/"
    data = [
        EdgePollingEvent.SERVER_SYSTEM_INFORMATION.value,
        EdgePollingEvent.SERVER_NETWORK_CONFIGURATION.value
    ]

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST request successful")
    else:
        print("POST request failed")

@shared_task
def aasx_client_polling():
    print("aasx_client_polling")
    url = f"{settings.CLIENT_URL}/periodic_task/"
    data = [
        EdgePollingEvent.CLIENT_SYSTEM_INFORMATION.value
    ]

    response = requests.post(url, json=data)
    print(response.status_code)
    if response.status_code == 200:
        print("POST request successful")
    else:
        print("POST request failed")
    
