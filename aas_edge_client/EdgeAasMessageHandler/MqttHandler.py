from abc import ABC, abstractmethod #Abstract Base Class
import paho.mqtt.client as mqtt_client
from typing import List, Dict, Any, Optional, Callable

class IMqttHandler(ABC):

    @abstractmethod
    def connect(self, host: str, port: int = 1883, keepalive: int = 60) -> bool:
        """ 
        Connect to an MQTT broker.

        Parameters:
            - host: The hostname or IP address of the MQTT broker.
            - port: The port number to connect to. Default is 1883.
            - keepalive: Maximum period in seconds between communications with the broker.
        
        Returns:
            - True if connection was successful, False otherwise.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnect from the MQTT broker.
        """
        pass

    @abstractmethod
    def subscribe(self, topic: str, qos: int = 0) -> None:
        """
        Subscribe to a topic to receive messages from the broker.

        Parameters:
            - topic: The topic to subscribe to.
            - qos: Quality of Service level. Can be 0, 1, or 2.
        """
        pass

    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        """
        Unsubscribe from a topic.

        Parameters:
            - topic: The topic to unsubscribe from.
        """
        pass

    @abstractmethod
    def publish(self, topic: str, payload: Optional[str], qos: int = 0, retain: bool = False) -> None:
        """
        Publish a message to a topic.

        Parameters:
            - topic: The topic on which the message should be published.
            - payload: The message payload.
            - qos: Quality of Service level. Can be 0, 1, or 2.
            - retain: If True, the message will be set as the "last known good" value for this topic.
        """
        pass

    @abstractmethod
    def set_message_callback(self, callback: Callable[[str, str], None]) -> None:
        """
        Set a callback function to handle incoming messages.

        Parameters:
            - callback: The function that will be called when a message arrives. The function should accept two parameters:
                        1. The topic name.
                        2. The message payload.
        """
        pass

class MqttHandler(IMqttHandler):
    def __init__(self) -> None:
        self._client = mqtt_client.Client()
        self._client.on_message = self._on_message

    def _on_message(self, client, userdata, message) -> None:
        if self._message_callback:
            self._message_callback(message.topic, message.payload.decode())

    def connect(self, host: str, port: int = 1883, keepalive: int = 60) -> bool:
        try:
            self._client.connect(host, port, keepalive)
            return True
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            return False

    def disconnect(self) -> None:
        self._client.disconnect()

    def subscribe(self, topic: str, qos: int = 0) -> None:
        self._client.subscribe(topic, qos)

    def unsubscribe(self, topic: str) -> None:
        self._client.unsubscribe(topic)

    def publish(self, topic: str, payload: Optional[str], qos: int = 0, retain: bool = False) -> None:
        self._client.publish(topic, payload, qos, retain)

    def set_message_callback(self, callback: Callable[[str, str], None]) -> None:
        self._message_callback = callback

    def loop_start(self) -> None:
        """Start the loop to process received messages."""
        self._client.loop_start()

    def loop_stop(self) -> None:
        """Stop the loop that processes received messages."""
        self._client.loop_stop()
