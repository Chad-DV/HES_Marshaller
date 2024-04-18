import socket
import ssl
import time
from datetime import datetime
from dataclasses import dataclass

import paho.mqtt.client as mqtt

@dataclass
class MQTTClient:
    host_address: str
    client_id: str
    username: str
    password: str
    topic: str
    host_port: int = 1883
    qos: int = 2

    def __post_init__(self):
        # Remove default values for optional parameters if they are not provided
        self.__dict__.update((k, v) for k, v in self.__dict__.items() if v != '')

# Setting SSL context
def set_ssl_context(client: mqtt.Client):
    context = ssl.create_default_context()
    context.options &= ssl.OP_NO_TLSv1
    context.options &= ssl.OP_NO_TLSv1_1
    client.tls_set_context(context)

# Create MQTT client setup
def create_mqtt_client(client_config: MQTTClient ,clean_session = False) -> mqtt.Client:
    client = mqtt.Client(client_id=client_config.client_id, clean_session=clean_session)
    client.username_pw_set(client_config.username, client_config.password)
    return client

# Set up message callbacks
def set_message_callback(client: mqtt.Client, client_config: MQTTClient, on_message_callback): 
    connected = False
    client.on_message = on_message_callback
    client.connect(client_config.host_address, port = client_config.host_port)
    client.subscribe(client_config.topic, qos=client_config.qos)
    while not connected:
        try:
            client.loop_forever()
            connected = True
        except socket.timeout:
            print(F"{datetime.now()} -> Connection timed out. Retrying in 5 minutes...")
            time.sleep(300)  # 5 minutes delay before retrying
        except Exception as e:
            print(f"Error: {e}")
            break

# Publish MQTT message
def publish_message(payload,username,client_config: MQTTClient):
    client = mqtt.Client()
    client.username_pw_set(username,client_config.password)
    client.connect(client_config.host_address, port = client_config.host_port)
    time.sleep(1)
    client.publish(client_config.topic, payload)
    client.disconnect()