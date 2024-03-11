from pymongo.collection import Collection
import typing
from utility.utility import encode_base64url
import requests
import json
import concurrent.futures
from functools import partial
from reactor.reactor import AsyncReactor
from reactor.handler import HandlerTypeName, Job
import asyncio
from reactor import REACTOR

reactor = REACTOR
# FETCHING from server
def read_content_of_table(collectionName: Collection, tableName: str) -> typing.Dict[str,str]:
    table_content = collectionName.find_one(
        {"_id": tableName},
        {"_id": 0}
    )
    return table_content

def extract_key_value(jsonData: typing.Dict[str,str]) -> typing.Tuple[typing.List[str], typing.List[str]]:
    # # Old version
    # key_dictionary = []
    # value_dicitionary = []
    # for key, value in jsonData.items():
    #     key_dictionary.append(key)
    #     value_dicitionary.append(value)
    # return (key_dictionary, value_dicitionary)
    
    # New Version
    keys, values = zip(*jsonData.items()) if jsonData else ([], [])
    return list(keys), list(values)


# TODO: change if need aas_uid for url? only when concept of REST API for submodel is incorrect
def fetch_single_submodel(  submodel_id: str, submodels_collection: Collection , 
                            aasxServerUrl: str, aasIdShort:str):
    #submodel_url = aasxServerUrl + "submodels/" + encode_base64url(submodel_id)
    submodel_url = f"{aasxServerUrl}/submodels/{encode_base64url(submodel_id)}"
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
    

# PARSER
def clientJson_2_aasSM(clientJson: typing.Dict, templateJson: typing.List):
    '''Required inputResponse and templateJSON need to be same structure of submodelElements and Properties'''
    try:
        for element in templateJson:
            if element["modelType"] == "MultiLanguageProperty":
                languageList = []
                for language, text in clientJson[element["idShort"]].items():
                    languageList.append({"language": language, "text": text})
                element["value"] = languageList
            elif element["modelType"] == "Property":
                element["value"] = clientJson[element["idShort"]]
            elif element["modelType"] == "SubmodelElementCollection":
                clientJson_2_aasSM(clientJson[element["idShort"]], element["value"])
            else:
                pass
    except KeyError:
        raise KeyError(f"Key {element['idShort']} not found in RequestBody")
    except TypeError:
        raise TypeError(f"Type of {element['idShort']} is not match")
    
def aasSM_2_clientJson(submodelElements: typing.List[typing.Dict]) -> typing.Dict:
    clientJson = {} # init
    
    for element in submodelElements:
        if element["modelType"] == "MultiLanguageProperty":
            languageJson = {}
            for language in element["value"]:
                languageJson[language["language"]] = language["text"]
            clientJson[element["idShort"]] = languageJson
        elif element["modelType"] == "Property":
            clientJson[element["idShort"]] = element["value"]
        elif element["modelType"] == "SubmodelElementCollection":
            clientJson[element["idShort"]] = aasSM_2_clientJson(element["value"])
        else:
            pass    
    return clientJson

def update_aasx_server(json_data: typing.Dict, 
                       aas_uid: str, 
                       submodel_uid: str, 
                       aasx_server: str,
                       submodelElements: str = None) -> typing.Tuple[typing.Dict, int]:
    # encode base64
    aas_uid = encode_base64url(aas_uid)
    submodel_uid = encode_base64url(submodel_uid)

    if submodelElements is None:
        aasxUrl = f"{aasx_server}/shells/{aas_uid}/submodels/{submodel_uid}"
    else:
        aasxUrl = f"{aasx_server}/shells/{aas_uid}/submodels/{submodel_uid}/submodel-elements/{submodelElements}"
    
    json_data = json.dumps(json_data)

    response = requests.put(url=aasxUrl, data=json_data)

    if response.status_code == 204:
        return ({"message": f"Submodel to server updated successfully"}, 204)
    else:
        return ({"error": f"Failed to update submodel to server"}, 500)

def update_submodel(collectionName: Collection,
                    aas_id_short: str,
                    submodel_id_short: str,
                    aas_uid:str,
                    aasx_server: str,
                    updated_data: typing.Dict,
                    sync_with_server: bool = None) -> typing.Tuple[typing.Dict, int]:
    submodel_template = read_content_of_table(collectionName=collectionName,
                                                tableName=f"{aas_id_short}:{submodel_id_short}")
    if submodel_template is None:
        print("Submodel not found")
        return ({"error": "Submodel not found"},404)
    else:
        try:
            clientJson_2_aasSM(clientJson=updated_data, templateJson= submodel_template["submodelElements"])
        except KeyError as e:
            return ({"error": str(e)}, 500)
        insert_result = collectionName.update_one(
            {"_id": f"{aas_id_short}:{submodel_id_short}"},
            {"$set": submodel_template},
            upsert=True
        )
        if insert_result.acknowledged:
            if sync_with_server:
                submodel_dictionary = read_content_of_table(collectionName=collectionName,
                                                    tableName=f"{aas_id_short}:submodels_dictionary")
                submodel_uid = submodel_dictionary.get(submodel_id_short)
                # return update_aasx_server(json_data=submodel_template, aas_uid=aas_uid, submodel_uid=submodel_uid, aasx_server=aasx_server)
                # return ({"message": "Submodel updated successfully"}, 200)
                asyncio.run(reactor.add_job(Job(type_=HandlerTypeName.UPDATE_AASX_SUBMODEL_SERVER.value, 
                                               requestBody={"json_data": submodel_template, 
                                                            "aas_uid": aas_uid, 
                                                            "submodel_uid": submodel_uid, 
                                                            "aasx_server": aasx_server})))
                
            return ({"message": "Submodel updated successfully"}, 200)    
        else:
            return ({"error": "Failed to update submodel"}, 500)
        
async def async_update_submodel(collectionName: Collection,
                          aas_id_short: str,
                          submodel_id_short: str,
                          aas_uid: str,
                          aasx_server: str,
                          updated_data: typing.Dict,
                          sync_with_server: bool = None) -> typing.Tuple[typing.Dict, int]:
    # Assuming read_content_of_table is adapted for async operation
    submodel_template = await asyncio.to_thread(read_content_of_table, 
                                                collectionName, 
                                                f"{aas_id_short}:{submodel_id_short}")
    if submodel_template is None:
        print("Submodel not found")
        return ({"error": "Submodel not found"}, 404)
    else:
        try:
            # Assuming clientJson_2_aasSM can either be run synchronously without much delay, or made async
            clientJson_2_aasSM(clientJson=updated_data, templateJson=submodel_template["submodelElements"])
        except KeyError as e:
            return ({"error": str(e)}, 500)

        # Assuming update_one is adapted for async operation or you're using an async-compatible database client
        insert_result = await asyncio.to_thread(lambda: collectionName.update_one(
            {"_id": f"{aas_id_short}:{submodel_id_short}"},
            {"$set": submodel_template},
            upsert=True
        ))

        if insert_result.acknowledged:
            if sync_with_server:
                # Assuming read_content_of_table and any other database calls here are async
                submodel_dictionary = await asyncio.to_thread(  read_content_of_table,
                                                                collectionName,
                                                                f"{aas_id_short}:submodels_dictionary")
                submodel_uid = submodel_dictionary.get(submodel_id_short)

                # Properly handling async call to an external service or async job scheduling
                await reactor.add_job(Job(type_=HandlerTypeName.UPDATE_AASX_SUBMODEL_SERVER.value, 
                                          requestBody={"json_data": submodel_template, 
                                                       "aas_uid": aas_uid, 
                                                       "submodel_uid": submodel_uid, 
                                                       "aasx_server": aasx_server}))

            return ({"message": "Submodel updated successfully"}, 200)
        else:
            return ({"error": "Failed to update submodel"}, 500)

# Submodul Elements
def read_submodel_element(collectionName: Collection,
                          aas_id_short: str,
                          submodel_id_short: str, 
                          submodelElements: str) -> typing.Tuple[typing.Dict, int]:
    tableName = f"{aas_id_short}:{submodel_id_short}"
    submodel_template = read_content_of_table(collectionName=collectionName,
                                                tableName=tableName)
    if submodel_template is None:
        return ({"error": "Submodel not found"},404)
    submodel_element_collection = submodel_template.get("submodelElements")
    submodel_element_split = submodelElements.split(".")
    
    correct_submodel_element = "/"
    # iterate through submodel_element_split
    for submodel_element in submodel_element_split:
        for element in submodel_element_collection:
            if element["idShort"] == submodel_element:
                submodel_element_collection = element["value"]
                correct_submodel_element = correct_submodel_element + submodel_element + "." 
                break
        else:
            wrong_submodel_element = submodel_element
            break
    else:
        submodel_element_collection = aasSM_2_clientJson(submodel_element_collection)
        return (submodel_element_collection, 200)
    
    return ({"error": f"Submodel element {wrong_submodel_element} not found under {correct_submodel_element}"}, 404)
        

def update_submodel_element(collectionName: Collection, 
                            aas_id_short: str,
                            submodel_id_short: str, 
                            submodelElements: str, 
                            aas_uid:str,
                            aasx_server: str,
                            updated_data: typing.Dict | str, sync_with_server: bool = False) -> typing.Tuple[typing.Dict, int]:
    submodelIdTableName = f"{aas_id_short}:{submodel_id_short}"
    submodel_template = read_content_of_table(collectionName=collectionName,
                                                tableName=submodelIdTableName)
    if submodel_template is None:
        return ({"error": "Submodel not found"},404)
    else:
        submodel_element_collection = submodel_template.get("submodelElements")
        submodel_element_split = submodelElements.split(".")
        
        # iterate through submodel_element_split
        for submodel_element in submodel_element_split:
            for element in submodel_element_collection:
                if element["idShort"] == submodel_element:
                    if submodel_element == submodel_element_split[-1]:
                        # Parse the updated_data to aasSM
                        if isinstance(element["value"], str) and isinstance(updated_data, str):
                            element["value"] = updated_data
                        elif isinstance(element["value"], list) and isinstance(updated_data, dict):
                            try:
                                clientJson_2_aasSM(clientJson=updated_data, templateJson= element["value"])
                                requestBodyJson = element["value"]
                            except KeyError as e:
                                return ({"error": str(e)}, 500)
                        else:
                            return ({"error": "Updated data and submodel element type mismatch"}, 500)
                        insert_result = collectionName.update_one(
                            {"_id": submodelIdTableName},
                            {"$set": submodel_template},
                            upsert=True
                        )
                        if insert_result.acknowledged:
                            if sync_with_server:
                                # TODO: move submodel_dictionary to Handler?
                                submodel_dictionary = read_content_of_table(collectionName=collectionName,
                                                    tableName=f"{aas_id_short}:submodels_dictionary")
                                submodel_uid = submodel_dictionary.get(submodel_id_short)
                                # # encode base64
                                # aas_uid = encode_base64url(aas_uid)
                                # submodel_uid = encode_base64url(submodel_uid)

                                asyncio.run(reactor.add_job(Job(type_=HandlerTypeName.UPDATE_AASX_SUBMODEL_ELEMENT_SERVER.value, 
                                               requestBody={"json_data": submodel_template, 
                                                            "aas_uid": aas_uid, 
                                                            "submodel_uid": submodel_uid,
                                                            "submodelElements": submodelElements, 
                                                            "aasx_server": aasx_server})))
                            else:
                                return ({"message": f"Submodel element {submodel_element} updated successfully"}, 200)                            
                        else:
                            return ({"error": f"Failed to update submodel element {submodel_element}"}, 500)
                    else:
                        submodel_element_collection = element["value"]
                    break
            else:
                wrong_submodel_element = submodel_element
                break
        else:
            return ({"error": f"Submodel element {wrong_submodel_element} not found"}, 404)
        
        return ({"error": f"Submodel element {submodel_element} not found"}, 404)
    
def compare_dicts(template_data: typing.Dict, update_data: typing.Dict) -> typing.Tuple[bool, typing.Set[str]]:
    # if update data contain all the data in template data -> True
    set_template_data = set(template_data.keys())
    set_update_data = set(update_data.keys())
    # if set_template_data == set_update_data:
    if set_template_data.issubset(set_update_data):
        return True, None
    else:
        missing_keys = set_template_data - set_update_data
        return False, missing_keys
 
    
def update_template(template_data: typing.Dict, update_data: typing.Dict) -> typing.Dict:
    #Update only the key in template, keys not in template will be ignore
    return_data = template_data.copy()
    for key, value in update_data.items():
        if key in return_data:
            return_data[key] = value
    return return_data
    
def update_time_series_record_template(collectionName: Collection, 
                            aas_id_short: str,
                            aas_uid:str,
                            update_data: typing.Dict,
                            aasx_server: str,
                            sync_with_server: bool = None) -> typing.Tuple[typing.Dict, int]:
                             
    submodelIdTableName = f"{aas_id_short}:TimeSeries"
    submodel_template = read_content_of_table(collectionName=collectionName,
                                                tableName=submodelIdTableName)
    
    if submodel_template is None:
        return ({"error": "Submodel not found"},404)
    else:
        record_data_template, _ = get_aas_submodel_elements_template(submodel_template=submodel_template,
                                                     submodelElements="Metadata.Record")
        new_time_series_data_template = record_data_template.copy()
            
        time_series_template = aasSM_2_clientJson(new_time_series_data_template["value"])
        # return (record_template, 200)
        compare_result, missing_keys = compare_dicts(time_series_template, update_data)
        if not compare_result:
            return ({"error": f"Missing keys: {missing_keys}"}, 500)
        else:

            new_time_series_data = update_template(time_series_template, update_data)
            clientJson_2_aasSM(clientJson=new_time_series_data, templateJson= new_time_series_data_template["value"])
            
            # Increase RecordCount
            record_count, _ = get_aas_submodel_elements_template(submodel_template=submodel_template,
                                                        submodelElements="Segments.InternalSegment.RecordCount")
            record_number = str(int(record_count["value"]) + 1)
            
            record_count["value"] = record_number
            new_time_series_data_template["idShort"] = record_number
            internal_segment_records, _ = get_aas_submodel_elements_template(submodel_template=submodel_template,
                                                        submodelElements="Segments.InternalSegment.Records")
            internal_segment_records["value"].append(new_time_series_data_template)

            # print(aasSM_2_clientJson(submodel_template["submodelElements"]))
            
            insert_result = collectionName.update_one(
                {"_id": submodelIdTableName},
                {"$set": submodel_template},
                upsert=True
            )

            if insert_result.acknowledged:
                if sync_with_server:
                    submodel_dictionary = read_content_of_table(collectionName=collectionName,
                                                        tableName=f"{aas_id_short}:submodels_dictionary")
                    submodel_uid = submodel_dictionary.get("TimeSeries")

                    asyncio.run(reactor.add_job(Job(type_=HandlerTypeName.UPDATE_AASX_SUBMODEL_SERVER.value, 
                                               requestBody={"json_data": submodel_template, 
                                                            "aas_uid": aas_uid, 
                                                            "submodel_uid": submodel_uid, 
                                                            "aasx_server": aasx_server})))
                else:
                    return ({"message": f"Time series record updated successfully"}, 200)
            else:
                return ({"error": f"Failed to update time series record"}, 500)


            # print(record_count)
            # return (new_time_series_data, 200)
    
def get_aas_submodel_elements_template(submodel_template: typing.Dict
                                       , submodelElements: str) -> typing.Tuple[typing.Dict,int]:
    submodel_element_collection = submodel_template.get("submodelElements")
    submodel_element_split = submodelElements.split(".")

    for submodel_element in submodel_element_split:
        for element in submodel_element_collection:
            if element["idShort"] == submodel_element:
                if submodel_element == submodel_element_split[-1]:
                    return (element, 200)
                else:
                    submodel_element_collection = element["value"]
                break
        else:
            wrong_submodel_element = submodel_element
            return ({"error": f"Submodel element {submodel_element} not found"}, 404)
    else:
        return ({"error": f"Submodel element {wrong_submodel_element} not found"}, 404)
        
        
