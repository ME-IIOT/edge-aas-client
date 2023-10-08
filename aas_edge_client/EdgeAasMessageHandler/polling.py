#This polling file is used to poll the data from the edge device and send it to the cloud, and other way (standalone file)
import time
import base64
from .RestHandler import RestHandler
from submodels_template.parser_submodel import aas_SM_element_2_django_response
import json
class Polling:

    def __init__(self, extUrl: str, intUrl: str, stopEvent, interval: int):
        # better using MQTT, an MQTT server on AAS, if there is a change on it -> publish message to the broker, client on edge device will receive the message
        # if there is a change in id (change revision, version...) -> logic broken. Need mqtt notify the change
        self.extClient = RestHandler(baseUrl=extUrl)
        self.intClient = RestHandler(baseUrl=intUrl)
        self.stopEvent = stopEvent
        self.interval = interval

    # def get(self):
    #     pass

    # def post(self):
    #     pass

    # def put(self):
    #     pass

    def loop(self):
        while not self.stopEvent.is_set():
            self.update()
            time.sleep(self.interval)

    def update(self):
        polledSubmodelElement = [self.extClient.get(url='/aas/Murrelektronik_V000_CTXQ0_0100001_AAS/submodels/Configuration/elements/NetworkSetting/deep')["elem"]]
        translatedElement = json.dumps(aas_SM_element_2_django_response(polledSubmodelElement))
        # should not call API directly -> lead to recursive call

        self.intClient.patch('/api/interfaces/', data= json.loads(translatedElement), headers={'Content-Type': 'application/json'})

    def stop(self):
        self.stopEvent.set()