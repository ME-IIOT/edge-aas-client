AASX_SERVER = "https://ca-aasxserverv3-dev-001.yellowtree-6659c4fd.northeurope.azurecontainerapps.io/"
AAS_IDSHORT = "Murrelektronik_V000_CTXQ0_0100001_AAS"
AAS_IDENTIFIER = "https://aas.murrelektronik.com/V000-CTXQ0-0100001/aas/1/0"
AAS_ASSET_IDENTIFIER = "https://murrelektronik.com/v000-ctxq0-0100001"
from utility.onboarding import edge_device_onboarding
from utility.submodels import fetch_submodels
from pymongo import MongoClient
import os

#Onboarding

MONGO_URI = os.environ.get('MONGO_URI')
# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

# Onboarding
# edge_device_onboarding(aasxServerUrl=AASX_SERVER, aasIdentifier=AAS_IDENTIFIER, aasIdShort=AAS_IDSHORT, shells_collection=shells_collection, submodels_collection=submodels_collection)

fetch_submodels(collectionName=submodels_collection, aasxServerUrl=AASX_SERVER, aasIdShort=AAS_IDSHORT)