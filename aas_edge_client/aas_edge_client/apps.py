# aas_edge_client/apps.py

from django.apps import AppConfig
from EdgeAasMessageHandler.MessageHandler import RestMessageHandler, MqttMessageHandler
from EdgeAasMessageHandler.Reactor import Reactor

class AasEdgeClientConfig(AppConfig):
    name = 'aas_edge_client'

    def ready(self):
        # Create and set the Reactor global variable
        global reactor
        reactor = Reactor()

        # Create an instance of RestMessageHandler with a base URL
        rest_handler = RestMessageHandler(baseUrl='http://repository.aas.dev.iot.murrelektronik.com') #TODO: replace with Environment Variable of docker
        mqtt_handler = MqttMessageHandler()
        #TODO: connect mqtt

        # Register the handlers with the reactor
        reactor.register_handler('rest', rest_handler)
        reactor.register_handler('mqtt', mqtt_handler)
