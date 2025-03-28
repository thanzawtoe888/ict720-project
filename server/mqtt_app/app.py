import paho.mqtt.client as mqtt
from datetime import datetime
import urllib3
import json
import os
import sys
import sqlite3
from pymongo import MongoClient
import joblib
import numpy as np

# initialize environment variables
mongo_uri = os.getenv('MONGO_URI', None)
mongo_db = os.getenv('MONGO_DB', None)
mongo_col_device = os.getenv('MONGO_COL_DEV', None)
mongo_col_user = os.getenv('MONGO_COL_USER', None)
mqtt_broker = os.getenv('MQTT_BROKER', None)
mqtt_port = os.getenv('MQTT_PORT', None)
mqtt_topic = os.getenv('MQTT_TOPIC', None)

if mongo_uri is None or mqtt_broker is None or mqtt_port is None or mqtt_topic is None:
    print('MONGO_URI and MQTT settings are required')
    sys.exit(1)

# initialize app
mongo_client = MongoClient(mongo_uri)

# Load the trained model and scaler
model = joblib.load('classification_model.pkl')
scaler = joblib.load('scaler.pkl')

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
    if msg.topic.split('/')[-1] == "request":
        db = mongo_client[mongo_db]
        print("Users in the database:")
        collection = db['user']
        results = list(collection.find())
        formatted_data = "\n".join([f"{user.get("user_id")}. {user.get("first_name")} {user.get("last_name")}" for user in results]) 
        client.publish("ict720/group8/user_list", formatted_data)
        
        # Insert MongoDB data into SQLite
        for user in results:
            try:
                # Prepare the data (use .get() to avoid KeyError if a field is missing)
                user_id = user.get('user_id', None)  # Use MongoDB's _id field as PRIMARY KEY
                first_name = user.get('first_name', None)
                last_name = user.get('last_name', None)
                
                # Insert into SQLite
                c.execute('''
                    INSERT OR REPLACE INTO user (user_id, first_name, last_name)
                    VALUES (?, ?, ?);
                ''', (user_id, first_name, last_name))
                
            except Exception as e:
                print(f"Error inserting user {user.get('_id')}: {e}")
        
        
    
    if msg.topic.split('/')[-1] == "register":
        data = json.loads(msg.payload.decode())
        
        # Get row count before insertion
        c.execute("SELECT COUNT(*) FROM user")
        row_count = c.fetchone()[0]  # Fetch the count result

        # insert to SQLite
        first_name = data['first_name']
        last_name = data['last_name']
        user_id = row_count
        c.execute("INSERT INTO user (user_id, first_name, last_name) VALUES (?, ?, ?)", (user_id, first_name, last_name))
        print("Inserted to SQLite")
        conn.commit()
        
        # insert to MongoDB
        db = mongo_client[mongo_db]
        db_user_col = db[mongo_col_user]
        db_user_col.insert_one({"timestamp": datetime.now(), 
                               "user_id": user_id,
                               "first_name": first_name, 
                               "last_name": last_name})
        print(db_user_col.count_documents({}))
        print("Inserted to MongoDB")
        
    if msg.topic.split('/')[-1] == "data":
        data = json.loads(msg.payload.decode())
        # insert to SQLite
        spo2 = data['spo2']
        bpm = data['bpm']
        user_id = data['user_id']
        excercise_mode = data['excercise_mode']
        c.execute("INSERT INTO health_data (user_id, spo2, bpm) VALUES (?, ?, ?)", (user_id, spo2, bpm))
        print("Inserted to SQLite")
        conn.commit()
        # insert to MongoDB
        db = mongo_client[mongo_db]
        db_dev_col = db[mongo_col_device]
        db_dev_col.insert_one({"timestamp": datetime.now(), 
                               "user_id": user_id,
                               "spo2": spo2, 
                               "bpm": bpm,
                               "excercise_mode": excercise_mode})
        print(db_dev_col.count_documents({}))
        print("Inserted to MongoDB")
        
        new_data = np.array([[spo2, bpm]])
        new_data_scaled = scaler.transform(new_data)
        prediction = model.predict(new_data_scaled)
        if prediction[0] == 1:
            exc_mode = "Running"
        elif prediction[0] == 2:
            exc_mode = "Walking"
        print("Predicted excercise mode:", exc_mode)

# Initialize SQLite
conn = sqlite3.connect(mongo_db)
c = conn.cursor()

# Enable foreign keys (optional but recommended)
c.execute("PRAGMA foreign_keys = ON;")
c.execute('''
    CREATE TABLE IF NOT EXISTS user (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_id TEXT UNIQUE NOT NULL,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        height INTEGER,
        weight INTEGER,
        emergency_contact TEXT
    )''')
conn.commit()

c.execute('''
    CREATE TABLE IF NOT EXISTS health_data (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_id TEXT NOT NULL,
        spo2 INTEGER,
        bpm FLOAT,
        excercise_mode INYEGER,
        FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
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