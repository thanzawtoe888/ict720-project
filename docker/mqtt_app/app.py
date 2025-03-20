import paho.mqtt.client as mqtt
from datetime import datetime
import urllib3
import json
import os
import sys
import sqlite3
from pymongo import MongoClient

# initialize environment variables
mongo_uri = os.getenv('MONGO_URI', None)
mongo_db = os.getenv('MONGO_DB', None)
mongo_col_device = os.getenv('MONGO_COL_DEV', None)
mqtt_broker = os.getenv('MQTT_BROKER', None)
mqtt_port = os.getenv('MQTT_PORT', None)
mqtt_topic = os.getenv('MQTT_TOPIC', None)
if mongo_uri is None or mqtt_broker is None or mqtt_port is None or mqtt_topic is None:
    print('MONGO_URI and MQTT settings are required')
    sys.exit(1)

# initialize app
mongo_client = MongoClient(mongo_uri)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_topic + "#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # data message
    if msg.topic.split('/')[-1] == "data":
        data = json.loads(msg.payload.decode())
        # print(f"Device: {data['name']}")
        # insert to SQLite
        spo2 = data['spo2']
        bpm = data['bpm']
        user_id = data['user_id']
        c.execute("INSERT INTO group8 (user_id, spo2, bpm) VALUES (?, ?, ?)", (user_id, spo2, bpm))
        print("Inserted to SQLite")
        conn.commit()
        # insert to MongoDB
        db = mongo_client[mongo_db]
        db_dev_col = db[mongo_col_device]
        db_dev_col.insert_one({"timestamp": datetime.now(), 
                               "user_id": user_id,
                               "spo2": spo2, 
                               "bpm": bpm})
        print(db_dev_col.count_documents({}))
        print("Inserted to MongoDB")

# init SQLite
conn = sqlite3.connect('group8.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS group8 (
          _id INTEGER PRIMARY KEY AUTOINCREMENT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          user_id STRING,
          spo2 INTEGER,
          bpm INTEGER
          )''')
conn.commit()

# init MQTT
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(mqtt_broker, int(mqtt_port), 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
mqttc.loop_forever()