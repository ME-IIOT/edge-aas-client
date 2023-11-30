from django.apps import AppConfig
from EdgeAasMessageHandler.Reactor import AsyncReactor
from django.conf import settings
from EdgeAasMessageHandler.EdgeSubmodelHandler import (UpdateServerSubmodelNetworkConfigurationHandler, 
                                                       UpdateServerSubmodelSystemInformationHandler,
                                                       EdgeUpdateSubmodelEvent)
from EdgeAasMessageHandler.EdgePollingHandler import (PollingSystemInformationServerHandler, 
                                                      PollingNetworkConfigurationServerHandler,
                                                      PollingSystemInformationClientHandler,
                                                      EdgePollingEvent)
import asyncio
from threading import Thread
from django.core.signals import request_finished
from django.dispatch import receiver
import atexit
import logging
import sys

logger = logging.getLogger('django')

class AasEdgeClientConfig(AppConfig):
    name = 'aas_edge_client'
    reactor_thread = None
    loop = None  # Added loop variable

    def ready(self):
        if 'celery' in sys.argv[0]:
            # Skip certain initializations if running in a Celery worker
            return
        
        self.reactor_thread = Thread(target=self.start_reactor, daemon=True) # Daemon threads are killed automatically when the main thread exits
        self.reactor_thread.start() # Start the thread
        atexit.register(self.on_exit) # Register a function to be called on exit of django project

    def start_reactor(self):
        async def start_reactor_async():
            try:
                reactor = AsyncReactor()

                # Register handlers
                reactor.register_handler(EdgeUpdateSubmodelEvent.NETWORK_CONFIGURATION.value  , UpdateServerSubmodelNetworkConfigurationHandler)
                reactor.register_handler(EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION.value     , UpdateServerSubmodelSystemInformationHandler)
                reactor.register_handler(EdgePollingEvent.SERVER_SYSTEM_INFORMATION.value     , PollingSystemInformationServerHandler)
                reactor.register_handler(EdgePollingEvent.SERVER_NETWORK_CONFIGURATION.value  , PollingNetworkConfigurationServerHandler)
                reactor.register_handler(EdgePollingEvent.CLIENT_SYSTEM_INFORMATION.value     , PollingSystemInformationClientHandler)

                await reactor.run()
            except Exception as e:
                logger.error(f"Exception occurred in reactor: {e}")
            finally:
                logger.info("Reactor has stopped.")
            # asyncio.create_task(reactor.run())
            # try:
            #     await asyncio.gather(reactor.run())
            # except Exception as e:
            #     print(f"Exception occurred in reactor: {e}")
            # finally:
            #     print("Reactor has stopped.")

        self.loop = asyncio.new_event_loop() # Create a new event loop
        asyncio.set_event_loop(self.loop) # Set the new event loop as the current one ? TODO: Not sure of this one
        self.loop.run_until_complete(start_reactor_async()) # Run the reactor in the event loop

    def on_exit(self):
        print("Shutting down: stopping reactor...")
        if self.reactor_thread and self.reactor_thread.is_alive():
            # Ensure reactor is stopped gracefully
            asyncio.run_coroutine_threadsafe(AsyncReactor().stop(), self.loop) 
            self.reactor_thread.join(timeout=1)  # Wait for the thread to finish in 1s, otherwise kill it
            print("Reactor thread stopped.")
    
    # @staticmethod
    # @receiver(request_finished) # request_finished is a signal that is sent when a Django HTTP request is finished -> not correct
    # def stop_reactor(sender, **kwargs):
    #     print("Attempting to stop reactor...")
    #     if AasEdgeClientConfig.reactor_thread and AasEdgeClientConfig.reactor_thread.is_alive():
    #         print("Sending stop command to reactor...")
    #         asyncio.run_coroutine_threadsafe(AsyncReactor().stop(), AasEdgeClientConfig.loop)
    #         AasEdgeClientConfig.reactor_thread.join()  # Ensure thread is properly joined
    #         print("Reactor thread stopped.")
    #     else:
    #         print("Reactor thread is not alive or already stopped.")

# class AasEdgeClientConfig(AppConfig):
#     name = 'aas_edge_client'
#     reactor_thread = None
#     def ready(self):
#         self.reactor_thread = Thread(target=self.start_reactor, daemon=True)
#         self.reactor_thread.start()

#         # Register a signal to stop the reactor on Django exit
#         request_finished.connect(self.stop_reactor)

#     def start_reactor(self):
#         async def start_reactor_async():
#             reactor = AsyncReactor()

#             # Register handlers
#             reactor.register_handler(EdgeUpdateSubmodelEvent.NETWORK_CONFIGURATION  , UpdateServerSubmodelNetworkConfigurationHandler)
#             reactor.register_handler(EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION     , UpdateServerSubmodelSystemInformationHandler)
#             reactor.register_handler(EdgePollingEvent.SERVER_SYSTEM_INFORMATION     , PollingSystemInformationServerHandler)
#             reactor.register_handler(EdgePollingEvent.SERVER_NETWORK_CONFIGURATION  , PollingNetworkConfigurationServerHandler)
#             reactor.register_handler(EdgePollingEvent.CLIENT_SYSTEM_INFORMATION     , PollingSystemInformationClientHandler)

#             asyncio.create_task(reactor.run())
#             # try:
#             #     await reactor.run()
#             # except Exception as e:
#             #     print(f"Exception occurred in reactor: {e}")
#             # finally:
#             #     print("Reactor has stopped.")

#         asyncio.run(start_reactor_async())

#     @staticmethod
#     @receiver(request_finished)
#     def stop_reactor(sender, **kwargs):
#         print("Stopping reactor...")
#         if AasEdgeClientConfig.reactor_thread and AasEdgeClientConfig.reactor_thread.is_alive():
#             asyncio.run(AsyncReactor().stop())

