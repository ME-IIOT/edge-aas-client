from submodels_template.parser_submodel import aas_SM_element_2_django_response
import json
from django.conf import settings
import logging
from datetime import datetime
import json

# Get an instance of a logger
logger = logging.getLogger('django')
from EdgeAasMessageHandler.EdgeHandler import EdgeHandler, Job, put_request, get_request, patch_request
import asyncio
import aiohttp

from typing import Dict, Type, List, Any
# from submodels_template.parser_submodel import django_response_2_aas_SM_element, ordered_to_regular_dict
from enum import Enum
async def run_bash_script(script):
    process = await asyncio.create_subprocess_exec('bash', script, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        logger.error(f'Error executing script: {stderr.decode()}')
        return None

    return stdout.decode()

class EdgePollingEvent(Enum):
    SERVER_NETWORK_CONFIGURATION    = "PollingNetworkConfigurationServerHandler"
    SERVER_SYSTEM_INFORMATION       = "PollingSystemInformationServerHandler"
    CLIENT_SYSTEM_INFORMATION       = "PollingSystemInformationClientHandler"

class PollingAASXServerHandler(EdgeHandler):
    submodelID: str

    async def handle(self, job: Job):
        print(f"PollingAASXServerHandler: {self.submodelID}")
        # request_data = job.requestBody
        try:
            async with aiohttp.ClientSession() as session:
                key, response = await get_request(session= session, 
                                    url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/{self.submodelID}/deep', 
                                    key = self.submodelID)
                
                polledFormat = response["content"].get("submodelElements", None)
                translatedFormat = self.translate_and_format(polledFormat, self.submodelID)

                await patch_request(session= session, 
                                    url = f'{settings.CLIENT_URL}/api/{self.submodelID}/', 
                                    data = translatedFormat, 
                                    key = self.submodelID)


        except aiohttp.ClientError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as e:
            logger.error(f"Error {e}. Check AASX file - {self.submodelID} submodel may missing element.")
            raise
    
    def translate_and_format(self, polled_data, data_type):
        translated_data = json.dumps(aas_SM_element_2_django_response(polled_data))
        data = json.loads(translated_data)
        try:
            # print("----------------------------retrieve LastUpdate from AAS server----------------------------------------")
            # print(data["LastUpdate"])
            datetime_obj = datetime.strptime(data["LastUpdate"], '%m/%d/%Y %H:%M:%S')
            data["LastUpdate"] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.exception(f"Failed to parse LastUpdate in {data_type}, using the current timestamp instead.")
            data["LastUpdate"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return data

class PollingNetworkConfigurationServerHandler(PollingAASXServerHandler):
    submodelID: str = "NetworkConfiguration"

class PollingSystemInformationServerHandler(PollingAASXServerHandler):
    submodelID: str = "SystemInformation"

class PollingAASXClientHandler(EdgeHandler):
    submodelID: str

class PollingSystemInformationClientHandler(PollingAASXClientHandler):
    submodelID: str = "SystemInformation"

    async def handle(self, job:Job):
        print(f"PollingSystemInformationClientHandler: {self.submodelID}")
        script_path = settings.STATIC_ROOT + '/mounted_script/sysInfo.sh'

        try:
            result = await run_bash_script(script_path)
            if result is None:
                return
            
            json_data = json.loads(result)

            logger.info('Successfully retrieved system information through bash script.')
            try:
                async with aiohttp.ClientSession() as session:
                    # await put_request(session= session, 
                    #                     url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/{self.submodelID}/elements/', 
                    #                     data = json_data, 
                    #                     key = self.submodelID)
                    await put_request(session= session, 
                                        url = f'{settings.CLIENT_URL}/api/{self.submodelID}/', 
                                        data = json_data, 
                                        key = self.submodelID)
            except aiohttp.ClientError as http_err:
                logger.error(f'Failed to update SystemInformation via API. Error: {http_err}')
                return    
        
        except json.JSONDecodeError as e:
            # print(f"JSONDecodeError: Error decoding the JSON file. {e}")
            logger.exception(f"Failed to parse json from script {script_path}")
            return
        except Exception as e:
            # print(f"An error occurred: {str(e)}")
            logger.exception(f"Failed to execute script {script_path}")
            return
    


    