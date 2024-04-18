import datetime
import json
import mysql.connector
from dataclasses import dataclass

@dataclass
class Database:
    host: str
    username: str
    password: str
    database_name: str
    table_name: str

def insert_data(json_string,database_settings:Database) -> bool:
    try:
        connection = mysql.connector.connect(
            host=database_settings.host,
            user=database_settings.username,
            password=database_settings.password,
            database=database_settings.database_name
        )

        # Parse the JSON string
        data = json.loads(json_string)
        
        # Extract values from the JSON data
        time_str = data['Time']
        kWh = float(data['kWh'])
        KVArh = float(data['KVArh'])
        meter_serial_number = int(data['MeterSerialNumber'])
        
        # Convert time string to datetime object
        time = datetime.datetime.strptime(time_str, "%m/%d/%y %I:%M:%S %p" if "AM" in time_str or "PM" in time_str else "%Y/%m/%d %H:%M:%S")
        
        # Prepare SQL query to insert data into the table
        cursor = connection.cursor()
        insert_query = f"INSERT INTO {database_settings.table_name} (MeterSerialNumber, Time, kWh, KVArh) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (meter_serial_number, time, kWh, KVArh))
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()