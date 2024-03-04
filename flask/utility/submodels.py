from pymongo.collection import Collection
import typing
from utility.utility import encode_base64url
import requests
import json
import concurrent.futures
from functools import partial

def read_content_of_table(collectionName: Collection, tableName: str) -> typing.Dict[str,str]:
    table_content = collectionName.find_one(
        {"_id": tableName},
        {"_id": 0}
    )
    return table_content

def extract_key_value(jsonData: typing.Dict[str,str]) -> typing.Tuple[typing.List[str], typing.List[str]]:
    key_dictionary = []
    value_dicitionary = []
    for key, value in jsonData.items():
        key_dictionary.append(key)
        value_dicitionary.append(value)
    return (key_dictionary, value_dicitionary)

def fetch_single_submodel(  submodel_id: str, submodels_collection: Collection , 
                            aasxServerUrl: str, aasIdShort:str):
    submodel_url = aasxServerUrl + "submodels/" + encode_base64url(submodel_id)
    response = requests.get(submodel_url)
    if response.status_code == 200:
        body = json.loads(response.text)
        submodelIdShort = body.get("idShort")
        insert_result = submodels_collection.update_one(
            {"_id": f"{aasIdShort}:{submodelIdShort}"},
            {"$set": body},
            upsert=True
        )
    else:
        print(f"Failed to fetch URL {submodel_url}. Status code:", response.status_code)
    pass

def fetch_submodels(collectionName: Collection, aasxServerUrl: str, aasIdShort: str):
    # read content -> Dict
    table_content = read_content_of_table(collectionName=collectionName, tableName=f"{aasIdShort}:submodels_dictionary")
    # read idShort -> List
    _, submodels_id= extract_key_value(table_content)
    # update each single submodel using ThreadPoolExecute
    fetch_func = partial(fetch_single_submodel, submodels_collection=collectionName, aasxServerUrl=aasxServerUrl, aasIdShort=aasIdShort)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_func, submodels_id)
    

