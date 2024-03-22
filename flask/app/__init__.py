from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os
import threading
import asyncio
from reactor.reactor import AsyncReactor
from reactor.handler import ( HandlerTypeName, 
                            UpdateAasxSubmodelElementServerHandler,
                            UpdateAasxSubmodelServerHandler,
                            TestHandler
                            )
from scheduler import  start_scheduler_async #start_scheduler,
from reactor import REACTOR
app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


def start_async_reactor():
    # Set up a new event loop for the background thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    reactor: AsyncReactor = REACTOR

    reactor.register_handler(HandlerTypeName.UPDATE_AASX_SUBMODEL_ELEMENT_SERVER.value, UpdateAasxSubmodelElementServerHandler)
    reactor.register_handler(HandlerTypeName.UPDATE_AASX_SUBMODEL_SERVER.value, UpdateAasxSubmodelServerHandler)
    reactor.register_handler(HandlerTypeName.TestHandler.value, TestHandler)

    loop.run_until_complete(reactor.run())

# @app.before_first_request
def activate_reactor():
    # Start the AsyncReactor in a background thread
    reactor_thread = threading.Thread(target=start_async_reactor, daemon=True)
    reactor_thread.start()

# def activate_scheduler():
#     scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
#     scheduler_thread.start()

def run_scheduler_async():
    # Set up the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_scheduler_async()

    loop.run_forever()

def activate_scheduler_async():
    # Run the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler_async, daemon=True)
    scheduler_thread.start()

# Load environment variables
MONGO_URI = os.environ.get('MONGO_URI')
print(MONGO_URI)
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
print(AAS_ID_SHORT)
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
print(AAS_IDENTIFIER)
AASX_SERVER = os.environ.get('AASX_SERVER')
print(AASX_SERVER)

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

from utility.onboarding import edge_device_onboarding

edge_device_onboarding(aasx_server=AASX_SERVER, aas_uid=AAS_IDENTIFIER, aas_id_short=AAS_ID_SHORT, 
                       shells_collection=shells_collection, submodels_collection=submodels_collection)

activate_reactor()
# activate_scheduler()
activate_scheduler_async()

from app import routes
