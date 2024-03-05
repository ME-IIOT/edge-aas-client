from utility.submodels import fetch_submodels
from pymongo import MongoClient
import os

# Load environment variables
MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

def polling_from_server() ->  None:
    # Fetch submodels
    print("Fetching submodels")
    fetch_submodels(collectionName=submodels_collection, aasxServerUrl=AASX_SERVER, aasIdShort=AAS_ID_SHORT)
    