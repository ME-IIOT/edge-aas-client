from flask import Flask
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
from scheduler import start_scheduler
from reactor import REACTOR
app = Flask(__name__)

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

def activate_scheduler():
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

# Load environment variables
MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

from utility.onboarding import edge_device_onboarding

edge_device_onboarding(aasxServerUrl=AASX_SERVER, aasIdentifier=AAS_IDENTIFIER, aasIdShort=AAS_ID_SHORT, 
                       shells_collection=shells_collection, submodels_collection=submodels_collection)

activate_reactor()
activate_scheduler()

from app import routes
