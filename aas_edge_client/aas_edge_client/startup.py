# myapp/startup.py

from threading import Thread, Event
import atexit
from EdgeAasMessageHandler.polling import Polling  # Ensure this import is correct

def start_polling():
    external_url = "http://localhost:51000"
    internal_url = "http://localhost:8000"
    stop_event = Event()
    polling_interval = 5  

    polling_instance = Polling(
        extUrl=external_url, 
        intUrl=internal_url, 
        stopEvent=stop_event,
        interval=polling_interval
    )
    
    # polling_thread = Thread(target=polling_instance.loop)
    # polling_thread.start()

    
    def graceful_stop():
        print("Stopping polling...")
        polling_instance.stop()
        print("Polling stopped.")
    
    atexit.register(graceful_stop)
    
    polling_thread = Thread(target=polling_instance.loop)
    polling_thread.start()
