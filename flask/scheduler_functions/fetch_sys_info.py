from pymongo import MongoClient
import os
from asgiref.sync import sync_to_async
from utility.submodels import read_content_of_table, fetch_single_submodel

MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

import asyncio
async def fetch_system_info_async():
    try:
        submodels_dictionary = await sync_to_async(read_content_of_table)(submodels_collection, f"{AAS_ID_SHORT}:submodels_dictionary")
        sysInfo_submodel_uid = submodels_dictionary.get("SystemInformation")
        status = await sync_to_async(fetch_single_submodel)(submodel_uid=sysInfo_submodel_uid,
                                                    submodels_collection=submodels_collection,
                                                    aasx_server=AASX_SERVER,
                                                    aasIdShort=AAS_ID_SHORT,
                                                    aas_uid=AAS_IDENTIFIER)
        if status:
            print("System Information fetched successfully")

    except Exception as e:
        print(f"Error executing update_system_info_async: {e}")