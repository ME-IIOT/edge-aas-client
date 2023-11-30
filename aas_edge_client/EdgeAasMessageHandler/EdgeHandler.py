import asyncio
import aiohttp
from abc import ABC, abstractmethod

from typing import Dict, Type, List, Any
from submodels_template.parser_submodel import django_response_2_aas_SM_element, ordered_to_regular_dict

from django.conf import settings

import logging
logger = logging.getLogger('django')

class Job:
    def __init__(self, type_: str, request_body: Dict):
        self.type = type_
        self.requestBody: Dict = request_body

class EdgeHandler(ABC):
    @abstractmethod
    async def handle(self, job: Job):
        raise NotImplementedError
    
    async def cleanup(self):
        pass

async def get_request(session: aiohttp.ClientSession, url: str, key: str) -> Dict[str, Any]:
    async with session.get(url, timeout=1) as response:
        if response.status != 200:
            logger.error(f"GET failed: {response.status} for key: {key} with URL: {url}")
            response.raise_for_status()
        return key, await response.json()

async def put_request(session: aiohttp.ClientSession, url: str, data: Dict[str, Any], key: str) -> None:
    async with session.put(url, json=data, timeout=1) as response:
        if response.status != 200:
            logger.error(f"PUT failed: {response.status} for key: {key} with URL: {url}")
            response.raise_for_status()

async def patch_request(session: aiohttp.ClientSession, url: str, data: Dict[str, Any], key: str) -> None:
    async with session.patch(url, json=data, timeout=1) as response:
        if response.status != 200:
            logger.error(f"PATCH failed: {response.status} for key: {key} with URL: {url}")
            response.raise_for_status()

