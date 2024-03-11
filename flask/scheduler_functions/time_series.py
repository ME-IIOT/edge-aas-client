from datetime import datetime
import os
from pymongo import MongoClient
import random

from utility.submodels import update_submodel
from utility.utility import run_command
# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']


from utility.submodels import update_time_series_record_template

def update_time_series_data():
    update_data = {'Time': str(datetime.now().isoformat()), 
                'SampleTemperature': str(random.randint(10, 20)),
                'SampleVoltage': str(random.uniform(23.5, 24.5)), 
                'SampleCurrent': '4'}
    update_time_series_record_template(collectionName=submodels_collection, 
                                                         aas_id_short=AAS_ID_SHORT,
                                                         aas_uid=AAS_IDENTIFIER,
                                                         update_data= update_data,
                                                         sync_with_server=True,
                                                         aasx_server=AASX_SERVER)
