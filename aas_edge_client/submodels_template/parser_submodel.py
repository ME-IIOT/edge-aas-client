import json

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

"value of elem key is in submodel/<submodel_id>/elements/<elem_id>/deep is a dictionary, but put it in a list (only 1 element) to match the recursive structure"
def django_response_2_aas_SM_element(djangoJSON, templateJSON):
    '''Required inputResponse and templateJSON need to be same structure of submodelElements and Properties'''
    
#    for key, value in inputResponseJSON.items():
    for index, (key, value) in enumerate(djangoJSON.items()):
        if isinstance(value, dict):
            django_response_2_aas_SM_element(value, templateJSON[index]["value"])
        else:
            templateJSON[index]["value"] = value

    return templateJSON
        

def aas_SM_element_2_django_response(templateJSON):
    #Recursive
    # for element in inputResponseJSON: # for the SubmodelElements, there is only one element, but need to do this for recursive function
    #     for elementKey, elementValue  in element.items():
    djangoJSON = {} # init
    for element in templateJSON:
        if isinstance(element["value"], list):
            djangoJSON[element["idShort"]] = aas_SM_element_2_django_response(element["value"])
        else:
            djangoJSON[element["idShort"]] = element["value"]

    return djangoJSON

inputResponseJSON = []
with open("inputJSON.json", 'r') as file:
    inputResponseJSON = json.load(file)


outputResponseJSON = []
with open("NetworkSetting.json", 'r') as file:
    outputResponseJSON = json.load(file)

# print(inputResponseJSON)
# print(outputResponseJSON)

# print(json.dumps(django_response_2_aas_SM_element(inputResponseJSON, outputResponseJSON)))
print(json.dumps(aas_SM_element_2_django_response(outputResponseJSON)))


    
    
