from utility.utility import encode_base64url, extract_submodels_id
import typing
import requests
# import time
# import asyncio
# import aiohttp
import json
import concurrent.futures
from pymongo.collection import Collection
from functools import partial

# to iterate through submodels_id the submodels and fetch the submodels
# submodel_id need to be the 1st parameter
def first_fetch_single_submodel(   submodel_uid: str, submodels_collection: Collection , 
                            aasxServerUrl: str, aasIdShort:str,
                            submodels_dictionary: typing.Dict[str, str],
                            aas_uid: str):
    # submodel_url = aasxServerUrl + "submodels/" + encode_base64url(submodel_id)
    submodel_url = f"{aasxServerUrl}/shells/{encode_base64url(aas_uid)}/submodels/{encode_base64url(submodel_uid)}"
    response = requests.get(submodel_url)
    if response.status_code == 200:
        body: typing.Dict = json.loads(response.text)
        submodelIdShort = body.get("idShort")
        insert_result = submodels_collection.update_one(
            {"_id": f"{aasIdShort}:{submodelIdShort}"},
            {"$set": body},
            upsert=True
        )
        submodels_dictionary[submodelIdShort] = submodel_uid
    else:
        print(f"Failed to fetch URL {submodel_url}. Status code:", response.status_code)

def onboarding_submodels(aasxServerUrl: str, aasIdShort: str, submodels_id: typing.List[str], submodels_collection: Collection, aas_uid: str):
    submodels_dictionary = {}
    
    # Using partial to bind submodels_collection parameter to fetch_submodel
    fetch_func = partial(first_fetch_single_submodel, submodels_collection=submodels_collection, submodels_dictionary=submodels_dictionary, 
                                                aasxServerUrl=aasxServerUrl, aasIdShort=aasIdShort, aas_uid = aas_uid)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        #only 1 iterator each function
        executor.map(fetch_func, submodels_id)
    insert_result = submodels_collection.update_one(
        {"_id": f"{aasIdShort}:submodels_dictionary"},  
        {"$set": submodels_dictionary},  
        upsert=True
    )
    
def edge_device_onboarding(aasx_server: str, aas_uid: str, aas_id_short: str, 
                           shells_collection: Collection, submodels_collection: Collection):
    # url = aasxServerUrl + "shells/" + encode_base64url(aasIdentifier)
    url = f"{aasx_server}/shells/{encode_base64url(aas_uid)}"
    # Send GET request
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        insert_data = json.loads(response.text)
        insert_result = shells_collection.update_one(
            {"_id": aas_id_short},  # Use _id field for a unique identifier
            {"$set": insert_data},  # Assuming you want to store the response in a field named "data"
            upsert=True
        )
        json_data = json.loads(response.text)
        submodels_id = extract_submodels_id(json_data)
        onboarding_submodels(aasIdShort= aas_id_short,submodels_id=submodels_id, submodels_collection=submodels_collection, aasxServerUrl=aasx_server, aas_uid=aas_uid)
    else:
        print("Failed to fetch URL. Status code:", response.status_code)