import random
import time
import json
from azure.iot.device import IoTHubDeviceClient, Message

# Replace with your IoT Hub device connection string
CONNECTION_STRING = "HostName=industrialiothub.azure-devices.net;DeviceId=simulatedpi;SharedAccessKey=0tAX5Hlh38P9J0P0RCcMrwYICzvwgoPEeG1T1Z5hgc0="
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(20, 80), 2),
        "vibration": round(random.uniform(0.1, 10.0), 2),
        "power_usage": round(random.uniform(50, 500), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def send_data():
    while True:
        sensor_data = generate_sensor_data()
        message = Message(json.dumps(sensor_data))
        print(f"Sending data: {sensor_data}")
        client.send_message(message)
        # Send data every 5 seconds
        time.sleep(5)  

if __name__ == "__main__":
    send_data()
