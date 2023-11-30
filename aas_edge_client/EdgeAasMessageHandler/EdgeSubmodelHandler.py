from EdgeAasMessageHandler.EdgeHandler import EdgeHandler, Job, put_request, get_request
import asyncio
import aiohttp

from typing import Dict, Type, List, Any
from submodels_template.parser_submodel import django_response_2_aas_SM_element, ordered_to_regular_dict

from django.conf import settings

import logging
logger = logging.getLogger('django')

from enum import Enum
class EdgeUpdateSubmodelEvent(Enum):
    NETWORK_CONFIGURATION   = "UpdateServerSubmodelNetworkConfigurationHandler"
    SYSTEM_INFORMATION      = "UpdateServerSubmodelSystemInformationHandler"

#TODO: function to check the format if the job same as in the AASX file
class UpdateServerSubmodelHandler(EdgeHandler):

    submodelID: str # short ID of submodel

    async def handle(self, job: Job):
        print(f"UpdateServerSubmodelHandler: {self.submodelID}")
        logger.info(f"UpdateServerSubmodelHandler: {self.submodelID}")
        request_data = job.requestBody
        try:
            async with aiohttp.ClientSession() as session:
                # Prepare GET requests
                get_tasks = [get_request(session= session, 
                                    url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/{self.submodelID}/elements/{key}/deep', 
                                    key = key) 
                                for key in request_data.keys()]

                # Run GET requests in parallel
                get_results = await asyncio.gather(*get_tasks)
                # print(get_results)

                # Prepare PUT requests based on GET responses
                put_tasks = []
                keys = []
                for key, response in get_results:
                    format = response["elem"]
                    to_translate_request_data = ordered_to_regular_dict({key: request_data[key]})
                    django_response_2_aas_SM_element(to_translate_request_data, [format])

                    put_url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/{self.submodelID}/elements/'
                    put_tasks.append(put_request(session, put_url, format, key))
                    keys.append(key)

                print(keys)
                # Run PUT requests in parallel
                await asyncio.gather(*put_tasks)

        except aiohttp.ClientError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return
        except Exception as e:
            logger.error(f"Error {e}. Check AASX file - {self.submodelID} submodel may missing element.")
            return

# TODO: Here is specific submodelID (static) -> for more dynamic, make SubmodelHandler by init get the submodelId as parameter
# change register_handler and get_handler of Reactor -> by create instance, transfer the submodelID
class UpdateServerSubmodelNetworkConfigurationHandler(UpdateServerSubmodelHandler):
    submodelID: str = "NetworkConfiguration"

class UpdateServerSubmodelSystemInformationHandler(UpdateServerSubmodelHandler):
    submodelID: str = "SystemInformation"

# TODO: SubmodelElementHandler -> change only one element of submodel (separate .py file)
# need to handel the Job.type to submodel path and element path (string split?)