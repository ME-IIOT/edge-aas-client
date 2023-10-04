from django.apps import AppConfig
from EdgeAasMessageHandler.MessageHandler import RestMessageHandler, MqttMessageHandler
from EdgeAasMessageHandler.Reactor import Reactor

class AasEdgeClientConfig(AppConfig):
    name = 'aas_edge_client'
    _reactor = None  # Store the reactor as a class-level attribute

    def ready(self):
        # Create and set the Reactor global variable
        self._reactor = Reactor()

        # Create an instance of RestMessageHandler with a base URL
        restHandler = RestMessageHandler(baseUrl='http://repository.aas.dev.iot.murrelektronik.com')
        mqttHandler = MqttMessageHandler()

        # Register the handlers with the reactor
        self._reactor.register_handler('rest', restHandler)
        self._reactor.register_handler('mqtt', mqttHandler)

    @property
    def reactor(self):
        return self._reactor
