import threading
import time
from django.apps import AppConfig
from EdgeAasMessageHandler.MessageHandler import RestMessageHandler, MqttMessageHandler
from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent
from EdgeAasMessageHandler.Reactor import Reactor

class AasEdgeClientConfig(AppConfig):
    name = 'aas_edge_client'
    _reactor = None  # Store the reactor as a class-level attribute
    _polling_started = False  # Add this flag

    def ready(self):
        # Start the delayed start_polling in a separate thread to avoid blocking
        
        threading.Thread(target=self.delayed_polling_start, daemon=True).start()

        # Create and set the Reactor global variable
        self._reactor = Reactor()

        # Create an instance of RestMessageHandler with a base URL
        restHandler = RestMessageHandler(baseUrl='http://localhost:51000')
        mqttHandler = MqttMessageHandler()
        edgeEventHandler = EdgeEventHandler()

        # Register the handlers with the reactor
        self._reactor.register_handler('rest', restHandler)
        self._reactor.register_handler('mqtt', mqttHandler)

        # Create and register EdgeEventHandlers with the reactor
        self._reactor.register_handler(EdgeEvent.INTERFACE_REQUEST, edgeEventHandler)

    def delayed_polling_start(self):
        # Delay to ensure server starts fully before polling begins
        time.sleep(5)  # Adjust delay as needed
        from .startup import start_polling
        start_polling()

    @property
    def reactor(self):
        return self._reactor
