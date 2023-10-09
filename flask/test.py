import requests
from parser_submodel import *

# Define the URL you want to send the GET request to
url1 = 'http://localhost:51000/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/deep'
url2 = 'http://localhost:51000/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels'

# Send a GET request
response = requests.get(url2)

# Check the response status code
if response.status_code == 200:
    # If the status code is 200, it means the request was successful
    # print("GET request to {} was successful.".format(url))
    print("Response Content:")
    response = submodels_transform_data(response.json(), baseURL= "")
    print(response)
    
    # submodelElements = response.json()["submodelElements"]
    # # submodelElements = aas_SM_element_2_django_response(submodelElements)
    # # submodelElements = django_response_2_name_value(submodelElements)
    # submodelElements = aas_SM_element_2_name_value(submodelElements)
    # print(json.dumps(submodelElements))

    # print(type(response))
else:
    # If the status code is not 200, there was an error
    print("GET request to {} failed with status code {}".format(url2, response.status_code))
