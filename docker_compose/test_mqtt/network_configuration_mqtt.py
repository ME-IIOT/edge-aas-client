import json
import paho.mqtt.client as mqtt

# Define the MQTT broker settings
broker = "localhost"
port = 1883

# Define the message payload
payload = {
    "NetworkSetting": {
        "InterfaceEth0": {
            "IPv4Address": "192.168.0.1",
            "IPv4SubnetMask": "255.255.255.0",
            "IPv4StandardGateway": "192.168.0.0",
            "Name": "eth0",
            "AddressMode": "Static",
            "LinkSpeedReceiveTransmit": "1 GBs",
            "IPv4DNSServers": "8.8.8.8",
            "PrimaryDNSSuffix": "www.murrelektronik.com"
        },
        "InterfaceEth1": {
            "IPv4Address": "192.168.1.100",
            "IPv4SubnetMask": "255.255.255.0",
            "IPv4StandardGateway": "192.168.1.0",
            "Name": "eth1",
            "AddressMode": "Automatic/DHCP",
            "LinkSpeedReceiveTransmit": "10 GBs",
            "IPv4DNSServers": "8.8.8.8",
            "PrimaryDNSSuffix": "www.murrelektronik.com"
        }
    },
    "LastUpdate": "2023-10-23T12:17:35Z"
}

# Create the MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # Subscribe to the topic
        client.subscribe("ServerNetworkConfigurationChange")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    print(f"Message received on {message.topic}")

# Set the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port)

# Start the client loop to handle callbacks
client.loop_start()

# Publish the message to the topic
client.publish("ClientNetworkConfigurationChange", json.dumps(payload))

# Keep the script running to process incoming messages
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Stop the client loop and disconnect
client.loop_stop()
client.disconnect()

import json
import paho.mqtt.client as mqtt

# Define the MQTT broker settings
broker = "localhost"
port = 1883

# Define the message payload
payload = {
    "NetworkSetting": {
        "InterfaceEth0": {
            "IPv4Address": "192.168.0.1",
            "IPv4SubnetMask": "255.255.255.0",
            "IPv4StandardGateway": "192.168.0.0",
            "Name": "eth0",
            "AddressMode": "Static",
            "LinkSpeedReceiveTransmit": "1 GBs",
            "IPv4DNSServers": "8.8.8.8",
            "PrimaryDNSSuffix": "www.murrelektronik.com"
        },
        "InterfaceEth1": {
            "IPv4Address": "192.168.1.100",
            "IPv4SubnetMask": "255.255.255.0",
            "IPv4StandardGateway": "192.168.1.0",
            "Name": "eth1",
            "AddressMode": "Automatic/DHCP",
            "LinkSpeedReceiveTransmit": "10 GBs",
            "IPv4DNSServers": "8.8.8.8",
            "PrimaryDNSSuffix": "www.murrelektronik.com"
        }
    },
    "LastUpdate": "2023-10-23T12:17:35Z"
}

# Create the MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # Subscribe to the topic
        client.subscribe("ServerNetworkConfigurationChange")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    print(f"Message received on {message.topic}")

# Set the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port)

# Start the client loop to handle callbacks
client.loop_start()

# Publish the message to the topic
client.publish("ClientNetworkConfigurationChange", json.dumps(payload))

# Keep the script running to process incoming messages
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Stop the client loop and disconnect
client.loop_stop()
client.disconnect()

