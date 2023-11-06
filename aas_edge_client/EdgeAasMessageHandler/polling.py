#This polling file is used to poll the data from the edge device and send it to the cloud, and other way (standalone file)
import time
from .RestHandler import RestHandler
from submodels_template.parser_submodel import aas_SM_element_2_django_response
import json
from django.conf import settings
from threading import Event
import subprocess
import logging
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger('django')
class AASX_Server_Polling:

    def __init__(self, extUrl: str, intUrl: str, stopEvent: Event, interval: int):
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
    
    # def update_NetworkConfiguration(self):
    #     logger.info("Polling NetworkConfiguration from Server")
    #     response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/deep')
    #     polledNetworkConfiguration = response["submodelElements"]
    #     translatedNetworkConfiguration = json.dumps(aas_SM_element_2_django_response(polledNetworkConfiguration))
        
    #     data_NetworkConfiguration = json.loads(translatedNetworkConfiguration)
        
    #     try:
    #         from datetime import datetime

    #         datetime_obj = datetime.strptime(data_NetworkConfiguration["LastUpdate"], '%m/%d/%Y %H:%M:%S')
    #         data_NetworkConfiguration["LastUpdate"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    #     except:
    #         data_NetworkConfiguration["LastUpdate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    #     self.intClient.patch('/api/NetworkConfiguration/',data=data_NetworkConfiguration, headers={'Content-Type': 'application/json'})

    # def update_SystemInformation(self):
    #     response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/deep')
    #     polledSystemInformation = response["submodelElements"]
    #     translatedSystemInformation = json.dumps(aas_SM_element_2_django_response(polledSystemInformation))
        
    #     data_SystemInformation = json.loads(translatedSystemInformation)
    #     try:
    #         from datetime import datetime

    #         datetime_obj = datetime.strptime(data_SystemInformation["LastUpdate"], '%m/%d/%Y %H:%M:%S')
    #         data_SystemInformation["LastUpdate"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    #     except:
    #         data_SystemInformation["LastUpdate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    #     self.intClient.patch('/api/SystemInformation/',data=data_SystemInformation, headers={'Content-Type': 'application/json'})

    def stop(self):
        self.stopEvent.set()

    def update_NetworkConfiguration(self):
        try:
            logger.info("Polling NetworkConfiguration from Server")
            response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/deep')
            if response["status_code"]!= 200:
                logger.error(f'Failed to poll NetworkConfiguration: {response["status_code"]} {response["content"]}')
                return

            polledNetworkConfiguration = response["content"].get("submodelElements")
            data_NetworkConfiguration = self.translate_and_format(polledNetworkConfiguration, "NetworkConfiguration")

            response = self.intClient.patch('/api/NetworkConfiguration/', data=data_NetworkConfiguration, headers={'Content-Type': 'application/json'})

            # if response["status_code"]not in range(200, 300):
            #     logger.error(f'Failed to update NetworkConfiguration from Server via API. Status Code: {response["status_code"]} Response: {response["content"]}')
        except Exception as e:
            logger.exception("An error occurred while updating NetworkConfiguration.")
            # raise exception as needed

    def update_SystemInformation(self):
        try:
            logger.info("Polling SystemInformation from Server")

            response = self.extClient.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/deep')
            if response["status_code"]!= 200:
                logger.error(f'Failed to poll SystemInformation: {response["status_code"]} {response["content"]}')
                return

            polledSystemInformation = response["content"].get("submodelElements")
            data_SystemInformation = self.translate_and_format(polledSystemInformation, "SystemInformation")

            response = self.intClient.patch('/api/SystemInformation/', data=data_SystemInformation, headers={'Content-Type': 'application/json'})

            # if response["status_code"] not in range(200, 300):
            #     logger.error(f'Failed to update SystemInformation from Server via API. Status Code: {response["status_code"]} Response: {response["content"]}')
        except Exception as e:
            logger.exception("An error occurred while updating SystemInformation.")
            # Handle the exception as needed

    def translate_and_format(self, polled_data, data_type):
        translated_data = json.dumps(aas_SM_element_2_django_response(polled_data))
        data = json.loads(translated_data)
        try:
            datetime_obj = datetime.strptime(data["LastUpdate"], '%m/%d/%Y %H:%M:%S')
            data["LastUpdate"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.exception(f"Failed to parse LastUpdate in {data_type}, using the current timestamp instead.")
            data["LastUpdate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return data


class ClientPolling:
    def __init__(self, intUrl: str , stopEvent: Event, interval: int):
        self.intClient = RestHandler(baseUrl=intUrl)
        self.stopEvent = stopEvent
        self.interval = interval

    def loop(self):
        while not self.stopEvent.is_set():
            self.update_SystemInformation()
            time.sleep(self.interval)

    # def update_SystemInformation(self):
    #     # Define the path to the script
    #     script_path = settings.STATIC_ROOT + '/mounted_script/sysInfo.sh'

    #     # Call the script using subprocess
    #     result = subprocess.run(['bash', script_path], capture_output=True, text=True)

    #     # Check for errors
    #     if result.returncode != 0:
    #         print(f'Error executing script: {result.stderr}')
    #         return

    #     # Print the JSON output
    #     json_output = json.loads(result.stdout)

    #     self.intClient.patch('/api/SystemInformation/',data=json_output, headers={'Content-Type': 'application/json'})

    def update_SystemInformation(self):
        # Define the path to the script
        script_path = settings.STATIC_ROOT + '/mounted_script/sysInfo.sh'

        try:
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)

            # Check for errors
            if result.returncode != 0:
                # Log error with the content of stderr
                logger.error(f'Error executing script: {result.stderr}')
                return
            
            try:
                json_output = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                # Log error with exception detail if JSON is invalid
                logger.error(f'Failed to parse JSON output: {e}')
                return

            logger.info('Successfully retrieved system information through bash script.')

            response = self.intClient.patch('/api/SystemInformation/', data=json_output, headers={'Content-Type': 'application/json'})
            
            if response["status_code"]not in range(200, 300):
                logger.error(f'Failed to update SystemInformation via API. Status Code: {response["status_code"]} Response: {response["content"]}')
        except Exception as e:
            logger.exception('An unexpected error occurred while retrieving SystemInformation in Client')

    def stop(self):
        self.stopEvent.set()

