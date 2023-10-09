import json
from collections import OrderedDict


def transform_response(inputResponse, templateFilePath):
    """
    Transforms the input_response based on a given template JSON file.

    :param input_response: dict, input response data to be transferred.
    :param template_json_file_path: str, file path to the template JSON structure to which data should be transferred.
    :return: dict, transformed JSON data.
    """
    try:
        # Load the template JSON data from the file
        with open(templateFilePath, 'r') as file:
            templateJson = json.load(file)
        
        # Transform the data
        for submodel in templateJson["submodelElements"]:
            for valueElement in submodel["value"]:
                keyName = valueElement["idShort"]
                
                # Ensure that key_name exists in input_response to prevent KeyErrors
                if keyName in inputResponse:
                    valueElement["value"] = inputResponse[keyName]

    except FileNotFoundError:
        print(f"FileNotFoundError: {templateFilePath} not found.")
        return None
    except KeyError as e:
        print(f"KeyError: {str(e)} is not a valid key.")
        return None
    except json.JSONDecodeError:
        print("JSONDecodeError: Error decoding the JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
    return templateJson

 # templateJSON is a in/out (reference) parameter
"value of elem key is in submodel/<submodel_id>/elements/<elem_id>/deep is a dictionary, but put it in a list (only 1 element) to match the recursive structure"
def django_response_2_aas_SM_element(djangoJSON, templateJSON):
    '''Required inputResponse and templateJSON need to be same structure of submodelElements and Properties'''
    for element in templateJSON:
        if isinstance(element["value"], list):
            django_response_2_aas_SM_element(djangoJSON[element["idShort"]], element["value"])
        else:
            element["value"] = djangoJSON[element["idShort"]]

        

def aas_SM_element_2_django_response(templateJSON):
    #Recursive
    # for element in inputResponseJSON: # for the SubmodelElements, there is only one element, but need to do this for recursive function
    
    djangoJSON = {} # init
    for element in templateJSON:
        if isinstance(element["value"], list):
            djangoJSON[element["idShort"]] = aas_SM_element_2_django_response(element["value"])
        else:
            djangoJSON[element["idShort"]] = element["value"]

    return djangoJSON

def ordered_to_regular_dict(ordered_dict):
    return {k: ordered_to_regular_dict(v) if isinstance(v, OrderedDict) else v for k, v in ordered_dict.items()}

def django_response_2_name_value(data, parent_key=None):
    new_data_list = []
    for key, value in data.items():
        new_data = {}
        if isinstance(value, dict) and value:  # checking if non-empty dict
            child_data = django_response_2_name_value(value, parent_key=key)
            new_data['name'] = key
            new_data['value'] = child_data
        else:
            new_data['name'] = key
            new_data['value'] = value if value else None  # avoid empty strings
        new_data_list.append(new_data)
    return new_data_list

def name_value_2_django_response(data_list):
    original_data = {}
    for item in data_list:
        key = item['name']
        value = item['value']
        
        if isinstance(value, list):
            # Recursive call to handle nested structure
            original_data[key] = name_value_2_django_response(value)
        else:
            original_data[key] = value
    
    return original_data

def aas_SM_element_2_name_value(data_list, baseURL):
    newList = []

    for data in data_list:
        newData = {}
        
        # Extract the name value and apply it to 'idShort'
        newData['name'] = data.get('idShort', None)
        newBaseURL = baseURL + "/" + newData['name']
        newData['link'] = newBaseURL
        
        # If 'value' key is a list, recursively apply the function
        if isinstance(data.get('value', None), list):
            newData['value'] = aas_SM_element_2_name_value(data['value'], baseURL=newBaseURL)
        # If 'value' key is a str or None, apply it directly
        else:
            newData['value'] = data['value'] if data['value'] else None
        
        newList.append(newData)
    
    return newList


def submodels_transform_data(data, baseURL):
    transformed = []
    
    for item in data:
        new_item = {
            "name": item.get("idShort", ""),
            "value": "",
            "link": baseURL + "/" + item.get("idShort", "")
        }
        transformed.append(new_item)
    
    return transformed
    
    
