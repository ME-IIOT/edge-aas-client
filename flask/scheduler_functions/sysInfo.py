import os
from pymongo import MongoClient

# Add the path to the sys.path list
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utility.submodels import update_submodel, async_update_submodel
from utility.utility import run_command, run_bash_script
# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

import asyncio
async def update_system_info_async():
    try:
        import os
        import json
        current_directory = os.getcwd()
        update_data = await run_bash_script(f"{current_directory}/scheduler_functions/mounted_script/sysInfo.sh")
        update_data = json.loads(update_data)
        await async_update_submodel(collectionName=submodels_collection,
                        aas_id_short= AAS_ID_SHORT,
                        submodel_id_short= "SystemInformation",
                        aas_uid=AAS_IDENTIFIER,
                        aasx_server=AASX_SERVER,
                        updated_data= update_data,
                        sync_with_server=True
                        )
    except Exception as e:
        print(f"Error executing update_system_info_async: {e}")
