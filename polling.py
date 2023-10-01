#This polling file is used to poll the data from the edge device and send it to the cloud, and other way (standalone file)

from EdgeAasClient.rest_client import RestClient
from EdgeAasClient.mqtt_client import MqttClient
class Polling:

    def __init__(self, ext_url: str, int_url: str):
        #this could be Mqtt client or Rest client (here we use rest client) -> need scheduler
        # better using MQTT, an MQTT server on AAS, if there is a change on it -> publish message to the broker, client on edge device will receive the message
        self.extClient = RestClient(base_url=ext_url)
        self.intClient = RestClient(base_url=int_url)
        self.notifyMqtt = MqttClient()
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

