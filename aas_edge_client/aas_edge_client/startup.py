# myapp/startup.py

from threading import Thread, Event
import atexit
from EdgeAasMessageHandler.polling import AASX_Server_Polling, ClientPolling  # Ensure this import is correct
from django.conf import settings

def start_polling():
    # URLs
    external_url = settings.SERVER_URL
    client_url = settings.CLIENT_URL

    # Common stop event
    stop_event = Event()

    # Server polling setup
    server_polling_interval = 10 
    server_polling = AASX_Server_Polling(
        extUrl=external_url, 
        intUrl=client_url, 
        stopEvent=stop_event,
        interval=server_polling_interval
    )

    # Client polling setup
    client_polling_interval = 5 
    client_polling = ClientPolling(
        intUrl=client_url, 
        stopEvent=stop_event,
        interval=client_polling_interval
    )

    # Graceful stop function
    def graceful_stop():
        print("Stopping polling...")
        server_polling.stop()
        client_polling.stop()
        print("Polling stopped.")

    # Register the graceful stop function
    atexit.register(graceful_stop)
    
    # Start server polling thread
    server_polling_thread = Thread(target=server_polling.loop)
    server_polling_thread.start()

    # Start client polling thread
    client_polling_thread = Thread(target=client_polling.loop)
    client_polling_thread.start()
