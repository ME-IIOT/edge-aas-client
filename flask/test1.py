
import requests
from parser_submodel import *

SERVER_URL = "http://localhost:51000"
AAS_IDSHORT = "Murrelektronik_V000_CTXQ0_0100001_AAS"

def collect_database_from_server():
    # get submodels
    print("Collecting data from server...")
    submodelsURL = SERVER_URL + "/aas/" + AAS_IDSHORT + "/submodels"
    response = requests.get(submodelsURL)
    gatewayDB = submodels_transform_data(response.json(), baseURL= "")
    for submodel in gatewayDB:
        submodelURL = SERVER_URL + "/aas/" + AAS_IDSHORT + "/submodels/" + submodel["name"] + "/deep"
        response = requests.get(submodelURL)
        submodel["value"] = submodelElements = aas_SM_element_2_name_value(response.json()["submodelElements"], submodel["link"])

    return gatewayDB

# print(json.dumps(collect_database_from_server()))
data = [
    {
        "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1",
        "name": "InterfaceEth1",
        "value": [
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1/IPv4Address",
                "name": "IPv4Address",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1/IPv4SubnetMask",
                "name": "IPv4SubnetMask",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1/Name",
                "name": "Name",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1/LinkSpeedReceiveTransmit",
                "name": "LinkSpeedReceiveTransmit",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1/IPv4DNSServers",
                "name": "IPv4DNSServers",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth1/PrimaryDNSSuffix",
                "name": "PrimaryDNSSuffix",
                "value": None
            }
        ]
    },
    {
        "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0",
        "name": "InterfaceEth0",
        "value": [
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0/IPv4Address",
                "name": "IPv4Address",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0/IPv4SubnetMask",
                "name": "IPv4SubnetMask",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0/Name",
                "name": "Name",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0/LinkSpeedReceiveTransmit",
                "name": "LinkSpeedReceiveTransmit",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0/IPv4DNSServers",
                "name": "IPv4DNSServers",
                "value": None
            },
            {
                "link": "/submodels/Configuration/elements/NetworkSetting/InterfaceEth0/PrimaryDNSSuffix",
                "name": "PrimaryDNSSuffix",
                "value": None
            }
        ]
    }
]

# print(name_value_2_django_response(data))
url = "http://localhost:51000/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/NetworkSetting/InterfaceEth1"

response = requests.delete(url)