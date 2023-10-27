from .EventHandler import EventHandler
from django.http import HttpRequest
from rest_framework.request import Request
from enum import Enum
from .RestHandler import RestHandler
from submodels_template.parser_submodel import django_response_2_aas_SM_element, ordered_to_regular_dict
import json
from django.conf import settings
import requests
from requests.exceptions import RequestException


# Event String definition
class EdgeEvent(Enum):
    INTERFACE_REQUEST = "interface_request"
    SENSOR_REQUEST = "sensor_request"
    HARDWARE_REQUEST = "hardware_request"
    NETWORK_CONFIGURATION_REQUEST = "network_configuration_request"
    SYSTEM_INFORMATION_REQUEST = "system_information_request"

# Handler base class for handling messages from the AAS Edge Client
class EdgeEventHandler(EventHandler):

    def handle_event(self, *args, **kwargs):
        # print("EdgeEventHandler.handle_event() called \n args: {} \n kwargs: {}".format(args, kwargs))
        
        request = kwargs.get('request', None)
        serializer_data = kwargs.get('serializer_data', None)
        event_name = kwargs.get('event_name', None)

        if all([request, serializer_data, event_name]):
            # print("All 'request', 'serializer.data', and 'event_name' are available.")
            
            methods_map = {
                # ('PUT', EdgeEvent.INTERFACE_REQUEST): self.handle_put_network_setting,
                # ('POST', EdgeEvent.INTERFACE_REQUEST): self.handle_put_network_setting,
                # ('PUT', EdgeEvent.SENSOR_REQUEST): self.handle_put_sensors,
                # ('POST', EdgeEvent.SENSOR_REQUEST): self.handle_put_sensors,
                # ('PUT', EdgeEvent.HARDWARE_REQUEST): self.handle_put_hardware,
                # ('POST', EdgeEvent.HARDWARE_REQUEST): self.handle_put_hardware,
                ('PUT', EdgeEvent.NETWORK_CONFIGURATION_REQUEST): self.handle_put_network_configuration,
                ('POST', EdgeEvent.NETWORK_CONFIGURATION_REQUEST): self.handle_put_network_configuration,
                ('PATCH', EdgeEvent.NETWORK_CONFIGURATION_REQUEST): self.handle_put_network_configuration,
                ('PUT', EdgeEvent.SYSTEM_INFORMATION_REQUEST): self.handle_put_system_information,
                ('POST', EdgeEvent.SYSTEM_INFORMATION_REQUEST): self.handle_put_system_information,
                ('PATCH', EdgeEvent.SYSTEM_INFORMATION_REQUEST): self.handle_put_system_information,
                # ('TBD', 'TBD'): self.handle_TBD,
                # Add additional methods as needed
            }
            
            method_handler = methods_map.get((request.method, event_name))
            
            if method_handler:
                # print("EdgeEventHandler.handle_event() called with {} request and {} event".format(request.method, event_name))
                return method_handler(request = request, request_data=serializer_data)
            else:
                print("Unsupported request method: {} or event name: {}".format(request.method, event_name))
        else:
            print("One or more of 'request', 'serializer.data', and 'event_name' are missing.")

    # def handle_put_network_setting(self, request, request_data ):
    #     # outputResponseJSON = []
    #     restHandler = RestHandler(baseUrl=settings.SERVER_URL)
    #     try:
    #         # add to list for recursive algorithm
    #         format = [restHandler.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/NetworkSetting/deep')["elem"]] #TODO: need some thing more dynamic
    #         restHandler.delete(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/NetworkSetting')
    #         request_data = ordered_to_regular_dict(request_data)
    #         django_response_2_aas_SM_element(request_data, format)
    #         # take 1st element because of recursive algorithm
    #         restHandler.put(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/', data=format[0])
    #         return True
    #     except:
    #         print("Error in EdgeEventHandler.handle_put_network_configuration()")
    
    # def handle_put_sensors(self, request, request_data ):
    #     restHandler = RestHandler(baseUrl=settings.SERVER_URL)
    #     try:
    #         # add to list for recursive algorithm
    #         format = [restHandler.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/ProcessData/elements/Sensors/deep')["elem"]] #TODO: need some thing more dynamic
    #         restHandler.delete(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/ProcessData/elements/Sensors')
    #         request_data = ordered_to_regular_dict(request_data)
    #         django_response_2_aas_SM_element(request_data, format)
    #         # take 1st element because of recursive algorithm
    #         restHandler.put(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/ProcessData/elements/', data=format[0])
    #         return True
    #     except:
    #         print("Error in EdgeEventHandler.handle_put_sensors()")

    # def handle_put_hardware(self, request, request_data):
    #     restHandler = RestHandler(baseUrl=settings.SERVER_URL)
    #     try:
    #         # add to list for recursive algorithm
    #         format = [restHandler.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/Hardware/deep')["elem"]] #TODO: need some thing more dynamic
    #         restHandler.delete(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/Hardware')
    #         request_data = ordered_to_regular_dict(request_data)
    #         django_response_2_aas_SM_element(request_data, format)
    #         # take 1st element because of recursive algorithm
    #         restHandler.put(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/', data=format[0])
    #         return True
    #     except:
    #         print("Error in EdgeEventHandler.handle_put_hardware()")

    # def handle_put_network_configuration(self, request, request_data):
    #     restHandler = RestHandler(baseUrl=settings.SERVER_URL)
    #     try:
    #         for key, value in request_data.items():
    #             format = [restHandler.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/{key}/deep')["elem"]] #TODO: need some thing more dynamic
    #             restHandler.delete(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/{key}')
    #             request_data = ordered_to_regular_dict({key:value})
    #             django_response_2_aas_SM_element(request_data, format)
    #             restHandler.put(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/', data=format[0])
    #     except Exception as e:
    #         print(f"error {e}")
    #         print("Error in EdgeEventHandler.handle_put_network_configuration()")
    #         print(key, value)
    #         print(request.data)

    # def handle_put_system_information(self,request, request_data):
    #     restHandlder = RestHandler(baseUrl=settings.SERVER_URL)
    #     try:
    #         for key, value in request_data.items():
    #             format = [restHandlder.get(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/{key}/deep')["elem"]]
    #             restHandlder.delete(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/{key}')
    #             request_data = ordered_to_regular_dict({key:value})
    #             django_response_2_aas_SM_element(request_data, format)
    #             restHandlder.put(url=f'/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/', data=format[0])
    #     except:
    #         print("Error in EdgeEventHandler.handle_put_system_information()")
    

    def handle_put_network_configuration(self, request, request_data):
        try:
            for key, value in request_data.items():
                # Construct the URL
                url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/{key}/deep'

                # Perform a GET request
                response = requests.get(url)

                #print(f"GET: {response.status_code}")
                if response.status_code != 200:
                    # Check for HTTP errors
                    response.raise_for_status()

                format = [response.json()["elem"]]
                
                request_data = ordered_to_regular_dict({key: value})
                django_response_2_aas_SM_element(request_data, format)

                # url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/{key}'
                # # Delete the resource
                # response = requests.delete(url)

                # #print(f"DEL: {response.status_code}")

                # if response.status_code != 200:
                #     # Check for HTTP errors
                #     response.raise_for_status()

                

                # Perform a PUT request
                url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/NetworkConfiguration/elements/'
                

                response = requests.put(url, json=format[0])
                
                #print(f"PUT: {response.status_code}")
                if response.status_code != 200:
                    # Check for HTTP errors
                    response.raise_for_status()

        except Exception as e:
            print(f"Error {e}. Check AASX file - NetworkConfiguration submodel may missing element.")
            raise e
        
    def handle_put_system_information(self, request, request_data):
        try:
            for key, value in request_data.items():
                # Construct the URL
                url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/{key}/deep'
                
                # Perform a GET request
                response = requests.get(url)

                # print(response.json())
                #print(f"GET: {response.status_code}")
                if response.status_code != 200:
                    # Check for HTTP errors
                    response.raise_for_status()
                format = [response.json()["elem"]]

                request_data = ordered_to_regular_dict({key: value})
                django_response_2_aas_SM_element(request_data, format)

                # url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/{key}'
                # # Delete the resource
                # response = requests.delete(url)
                

                # #print(f"DEL: {response.status_code}")
                # if response.status_code != 200:
                #     # Check for HTTP errors
                #     response.raise_for_status()



                # Perform a PUT request
                url = f'{settings.SERVER_URL}/aas/{settings.AAS_ID_SHORT}/submodels/SystemInformation/elements/'
                response = requests.put(url, json=format[0])

                
                #print(f"PUT: {response.status_code}")                
                if response.status_code != 200:

                    # Check for HTTP errors
                    response.raise_for_status()

        except Exception as e:
            print(f"Error {e}. Check AASX file - SystemInformation submodel may missing element.")
            raise e