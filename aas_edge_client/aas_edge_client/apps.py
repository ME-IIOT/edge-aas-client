import threading
import time
from django.apps import AppConfig
from EdgeAasMessageHandler.Reactor import Reactor
from EdgeAasMessageHandler.MqttHandler import MqttHandler
from django.conf import settings
import atexit
class AasEdgeClientConfig(AppConfig):
    name = 'aas_edge_client'
    # _reactor = None 

    def ready(self):
        # Start the delayed start_polling in a separate thread to avoid blocking
        threading.Thread(target=self.delayed_polling_start, daemon=True).start()

        # Create and set the Reactor global variable
        # self._reactor = Reactor()

    def delayed_polling_start(self):
        # Delay to ensure server starts fully before polling begins
        time.sleep(5)  # Adjust delay as needed
        from .startup import start_polling
        start_polling() 

    # @property
    # def reactor(self):
    #     return self._reactor
    
    
