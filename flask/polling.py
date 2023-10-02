#This polling file is used to poll the data from the edge device and send it to the cloud, and other way (standalone file)

from EdgeAasClient.RestClient import RestClient
from EdgeAasClient.MqttClient import MqttClient
import time
import base64
class Polling:

    def __init__(self, extUrl: str, intUrl: str, stopEvent):
        # better using MQTT, an MQTT server on AAS, if there is a change on it -> publish message to the broker, client on edge device will receive the message
        # if there is a change in id (change revision, version...) -> logic broken. Need mqtt notify the change
        self.extClient = RestClient(baseUrl=extUrl)
        self.intClient = RestClient(baseUrl=intUrl)
        self.notifyMqtt = MqttClient() #TODO
        self.stopEvent = stopEvent

    # def get(self):
    #     pass

    # def post(self):
    #     pass

    # def put(self):
    #     pass

    def loop(self):
        while not self.stopEvent.is_set():
            self.update()
            time.sleep(60) # Sleep for 1 minute

    def update(self):
        submodelIds = self.get_all_submodelIds()
        for submodelId in submodelIds:
            polledSubmodel = self.extClient.get(f'/submodels/{submodelId.decode()}')
            self.intClient.put(f'/submodels/{submodelId.decode()}', data=polledSubmodel)
            print("update submodel: ", base64.b64decode(submodelId).decode('utf-8'))

    def get_all_submodelIds(self):
        # Fetch all submodels from the MongoDB collection through internal client
        submodels = self.intClient.get('/submodels')
        submodels = submodels["submodels"]

        # Extract 'id' values and encode it, return them as a list
        idList = [base64.b64encode(submodel["id"].encode()) for submodel in submodels]

        return idList




