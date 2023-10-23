import json
import paho.mqtt.client as mqtt

# Define the MQTT broker settings
broker = "localhost"
port = 1883

# Define the message payload
payload = {
    "Hardware": {
        "Processor": {
            "CpuType": "ARMv8",
            "CpuCores": "4",
            "CpuClock": "1.8 GHz",
            "CpuUsage": "17 %",
            "CpuTemperature": "55 °C"
        },
        "Memory": {
            "RAMInstalled": "2 GB",
            "RAMFree": "729 MB",
            "DiskInstalled": "17 GB",
            "DiskFree": "14.3 GB"
        },
        "BoardTemperature": "42 °C"
    },
    "HealthStatus": "Normal",
    "LastUpdate": "2023-10-23T12:40:36Z"
}

# Create the MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # Subscribe to the topic
        client.subscribe("ServerSystemInformationChange")
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
client.publish("ClientSystemInformationChange", json.dumps(payload))

# Keep the script running to process incoming messages
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Stop the client loop and disconnect
client.loop_stop()
client.disconnect()

