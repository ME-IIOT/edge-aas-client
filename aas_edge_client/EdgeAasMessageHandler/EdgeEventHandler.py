from .EventHandler import EventHandler
from django.http import HttpRequest
from rest_framework.request import Request
from enum import Enum
from .RestHandler import RestHandler
from submodels_template.parser_submodel import django_response_2_aas_SM_element, ordered_to_regular_dict
import json
from django.conf import settings

print(settings.BASE_DIR)


# Event String definition
class EdgeEvent(Enum):
    INTERFACE_REQUEST = "interface_request"

# Handler base class for handling messages from the AAS Edge Client
class EdgeEventHandler(EventHandler):

    def handle_event(self, *args, **kwargs):
        print("EdgeEventHandler.handle_event() called \n args: {} \n kwargs: {}".format(args, kwargs))
        # return super().handle_event(*args, **kwargs)
        request = kwargs.get('request', None)
        serializer_data = kwargs.get('serializer_data', None)

        if request is not None and serializer_data is not None:
            print("Both 'request' and 'serializer.data' are available.")

            if request.method == 'PUT':
                print("EdgeEventHandler.handle_event() called with PUT request")
                # restHandler.delete(url='/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/NetworkSetting')
                # restHandler.put(url='/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/', data=request.data)
                return self.handle_put(request, request_data=serializer_data)

        else:
            print("'request' or 'serializer.data' is missing.")

    def handle_put(self, request, request_data ):
        # outputResponseJSON = []
        restHandler = RestHandler(baseUrl='http://localhost:51000')
        try:
            # add to list for recursive algorithm
            format = [restHandler.get(url='/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/NetworkSetting/deep')["elem"]] #TODO: need some thing more dynamic
            restHandler.delete(url='/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/NetworkSetting')
            request_data = ordered_to_regular_dict(request_data)
            # print(request_data)
            django_response_2_aas_SM_element(request_data, format)
            # print(format)
            # take 1st element because of recursive algorithm
            restHandler.put(url='/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/', data=format[0])
            return True
        except:
            print("Error in EdgeEventHandler.handle_put()")
        # return None
        # print(format["elem"])
        