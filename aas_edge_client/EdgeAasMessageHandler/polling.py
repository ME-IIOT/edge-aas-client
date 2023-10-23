#This polling file is used to poll the data from the edge device and send it to the cloud, and other way (standalone file)
import time
from .RestHandler import RestHandler
from submodels_template.parser_submodel import aas_SM_element_2_django_response
import json
from django.conf import settings
class Polling:

    def __init__(self, extUrl: str, intUrl: str, stopEvent, interval: int):
        # better using MQTT, an MQTT server on AAS, if there is a change on it -> publish message to the broker, client on edge device will receive the message
        # if there is a change in id (change revision, version...) -> logic broken. Need mqtt notify the change
        self.extClient = RestHandler(baseUrl=extUrl)
        self.intClient = RestHandler(baseUrl=intUrl)
        self.stopEvent = stopEvent
        self.interval = interval

    def loop(self):
        while not self.stopEvent.is_set():
            # self.update_interfaces()
            # self.update_hardware()
            self.update_NetworkConfiguration()
            self.update_SystemInformation()
            time.sleep(self.interval)

    def update_interfaces(self):
        response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/NetworkSetting/deep')
        polledNetworkSetting = [response["elem"]]
        translatedNetworkSetting = json.dumps(aas_SM_element_2_django_response(polledNetworkSetting))
        # should not call API directly -> lead to recursive call

        self.intClient.patch('/api/interfaces/', data= json.loads(translatedNetworkSetting), headers={'Content-Type': 'application/json'})

    def update_sensors(self):
        response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/ProcessData/elements/Sensors/deep')
        polledSensors = [response["elem"]]
        translatedSensors = json.dumps(aas_SM_element_2_django_response(polledSensors))
        # should not call API directly -> lead to recursive call

        self.intClient.patch('/api/sensors/', data= json.loads(translatedSensors), headers={'Content-Type': 'application/json'})

    def update_hardware(self):
        response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/Hardware/deep')
        polledHardware = [response["elem"]]
        translatedHardware = json.dumps(aas_SM_element_2_django_response(polledHardware))
        # should not call API directly -> lead to recursive call

        self.intClient.patch('/api/hardware/', data= json.loads(translatedHardware), headers={'Content-Type': 'application/json'})
    
    def update_NetworkConfiguration(self):
        response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/deep')
        polledNetworkConfiguration = response["submodelElements"]
        translatedNetworkConfiguration = json.dumps(aas_SM_element_2_django_response(polledNetworkConfiguration))
        
        data_NetworkConfiguration = json.loads(translatedNetworkConfiguration)
        
        try:
            from datetime import datetime

            datetime_obj = datetime.strptime(data_NetworkConfiguration["LastUpdate"], '%m/%d/%Y %H:%M:%S')
            data_NetworkConfiguration["LastUpdate"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            data_NetworkConfiguration["LastUpdate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        self.intClient.patch('/api/NetworkConfiguration/',data=data_NetworkConfiguration, headers={'Content-Type': 'application/json'})

    def update_SystemInformation(self):
        response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/deep')
        polledSystemInformation = response["submodelElements"]
        translatedSystemInformation = json.dumps(aas_SM_element_2_django_response(polledSystemInformation))
        
        data_SystemInformation = json.loads(translatedSystemInformation)
        try:
            from datetime import datetime

            datetime_obj = datetime.strptime(data_SystemInformation["LastUpdate"], '%m/%d/%Y %H:%M:%S')
            data_SystemInformation["LastUpdate"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            data_SystemInformation["LastUpdate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        self.intClient.patch('/api/SystemInformation/',data=data_SystemInformation, headers={'Content-Type': 'application/json'})

    def stop(self):
        self.stopEvent.set()

    