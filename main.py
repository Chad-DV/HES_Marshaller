import logging
import sys
import json
import os
import time

import powershare_marshaller_java_hes.mqtt_handler as mqtt
import powershare_marshaller_java_hes.database_handler as db

'''
This application acts as a middle man listening to a topic on a broker(SGate when this was written)
and then publishes those messages to a nother broker (Thingsboard at this time) and inserts that data into a MySQL DB

Created at: 28/02/2024

Author: chad.devilliers@igrid.co.za
'''

#get dir for main script
file_path = os.path.dirname(os.path.abspath(__file__))

#get eorking dir for contianer
container_working_dir = os.getcwd()

#-> setup log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(container_working_dir, "marshaller.log"))
    ]
)
# Callback function to handle message reception
def on_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    try:
        payload_dict = json.loads(payload)  # Parse the payload string to a dictionary
        modified_json_message, meter_serial_number = json_to_thingsboard_json(payload_dict)
        #To view the modified message
        #print("Modified JSON message:", modified_json_message)
        mqtt.publish_message(modified_json_message,meter_serial_number,publisher)
        db.insert_data(payload,database)
    except json.JSONDecodeError as e:
        print(e)
        logging.error(e)

def load_settings(file_path):
    with open(file_path, 'r') as f:
        settings = json.load(f)
    return settings

def json_to_thingsboard_json(original_message):
    try:
        # Extract time string
        time_str = original_message["Time"]
    
        format_str = "%m/%d/%y %I:%M:%S %p" if "AM" in time_str or "PM" in time_str else "%Y/%m/%d %H:%M:%S"
        time_struct = time.strptime(time_str, format_str)
        epoch_milliseconds = int((time.mktime(time_struct) * 1000) - (3600000*2))

        # Construct modified message
        modified_message = json.dumps({
            "ts": epoch_milliseconds,
            "values": {**original_message}
        })

        # Extract meter serial number
        meter_serial_number = original_message["MeterSerialNumber"]
    except Exception as e:
        print(e)
        return f'{"Error":"{e}"}',0
    return modified_message, meter_serial_number

def get_database_config(settings_dict) -> db.Database:
    database_settings = db.Database(
        settings_dict.get('host'),
        settings_dict.get('username'),
        settings_dict.get('password'),
        settings_dict.get('database_name'),
        settings_dict.get('table_name')
    )
    return database_settings

def get_mqtt_config(settings_dict) -> mqtt.MQTTClient:
    mqtt_client = mqtt.MQTTClient(
        settings_dict.get('host_address'),
        settings_dict.get('client_id'),
        settings_dict.get('username'),
        settings_dict.get('password'),
        settings_dict.get('topic'),
        settings_dict.get('port'),
        settings_dict.get('qos')
    ) 
    return mqtt_client

if __name__ == "__main__":

    settings = load_settings(os.path.join(file_path,'config.json'))

    database= get_database_config(settings['database'])
    subscriber = get_mqtt_config(settings['subscriber'])
    publisher = get_mqtt_config(settings['publisher'])

    mqtt_client = mqtt.create_mqtt_client(subscriber)
    mqtt.set_ssl_context(mqtt_client)
    mqtt.set_message_callback(mqtt_client, subscriber, on_mqtt_message)