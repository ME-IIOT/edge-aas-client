from abc import ABC, abstractmethod
from typing import List
from EdgeAasMessageHandler.MqttHandler import MqttHandler
from EdgeAasMessageHandler.RestHandler import RestHandler

# MessageHandler Interface
class MessageHandler(ABC):
    @abstractmethod
    def handle_message(self, request, *args, **kwargs):
        pass
    
# Implementation classes
class RestMessageHandler(MessageHandler, RestHandler):
    def __init__(self, baseUrl: str = ''):
        # Initialize RestHandler
        RestHandler.__init__(self, baseUrl)

    def handle_message(self, request, *args, **kwargs):
        # Assuming the request contains details about the request type, URL, data, headers etc.
        request_type = request.get('type').lower()
        url = request.get('url')
        data = request.get('data')
        headers = request.get('headers')
        
        if request_type == 'get':
            return self.get(url, params=data, headers=headers)
        elif request_type == 'post':
            return self.post(url, data=data, headers=headers)
        elif request_type == 'put':
            return self.put(url, data=data, headers=headers)
        elif request_type == 'delete':
            return self.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported request type: {request_type}")

class MqttMessageHandler(MessageHandler, MqttHandler):
    def handle_message(self, request, *args, **kwargs):
        pass #TODO
