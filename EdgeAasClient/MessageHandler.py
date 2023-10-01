from abc import ABC, abstractmethod
from typing import List
from EdgeAasClient.MqttClient import MqttClient
from EdgeAasClient.RestClient import RestClient

# MessageHandler Interface
class MessageHandler(ABC):
    @abstractmethod
    def handle_event(self, message):
        pass
    
# Implementation classes
class RestHandler(MessageHandler, RestClient):
    def handle_event(self, message):
        self.process_message(message)

class MqttHandler(MessageHandler, MqttClient):
    def handle_event(self, message):
        self.process_message(message)