from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import json
import os
import sys

# initialize environment variables
mongo_uri = os.getenv('MONGO_URI', None)
mongo_db = os.getenv('MONGO_DB', None)
mongo_col_device = os.getenv('MONGO_COL_DEV', None)
mongo_col_user = os.getenv('MONGO_COL_USER', None)
if mongo_uri is None or mongo_db is None or mongo_col_device is None or mongo_col_user is None:
    print('MONGO_URI is required')
    sys.exit(1)

# initialize app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

mongo_client = MongoClient(mongo_uri)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

print("Client: ", mongo_client, mongo_uri)

# Connect to Database
print("Connect to MongoDB")
db = mongo_client[mongo_db]
print("MongoDB connected, URI: ", mongo_uri, "  DataBase: ", db)

# User table
print("Connect to user table.")
users_collection = db[mongo_col_user]
print("User table connected.")

# Data table
print("Connect to data table.")
data_collection = db[mongo_col_device]
print("Data table connected.")

# Ensure collection exists
# if "users" not in db.list_collection_names():

# Ensure unique index
# Create a unique index on the username field to prevent duplicates
# print("Creating index in user table.")
# users_collection.create_index("username", unique=True)
# print("Success to create index user table.")



# REST API: user_id
@app.route('/api/user/<user_id>', methods=['GET'])
def query_station(user_id):
    resp = {}
    # extract parameters
    if user_id is None:
        resp['status'] = 'error'
        resp['message'] = 'user_id is required'
        return jsonify(resp)
    bpm_cond = int(request.args.get('bpm', 70))
    mins_cond = int(request.args.get('mins', 10))
    # database connection
    db = mongo_client[mongo_db]
    db_dev_col = db[mongo_col_device]
    print(db_dev_col.count_documents({}))
    # choose only valid data, sort by timestamp
    docs = db_dev_col.find({"user_id": user_id,
                            "timestamp": {"$gt": datetime.now() - timedelta(minutes=mins_cond)},
                            "bpm": {"$gt": bpm_cond}}).sort("timestamp", -1)
    resp['status'] = 'ok'
    resp['user_id'] = user_id
    resp['data'] = []
    users_id = []
    for doc in docs:
        if doc['user_id'] in users_id:
            continue
        users_id.append(doc['user_id'])
        doc_data = {}
        doc_data['timestamp'] = doc['timestamp'].isoformat()
        doc_data['bpm'] = doc['bpm']
        resp['data'].append(doc_data)
        print(resp['data'])
    return jsonify(resp)


@app.route('/register', methods=['POST'])
def register():
    print("Register endpoint hit.")

    data = request.json

    required_fields = ["username", "password", "email", "first_name", "last_name"]

    if not data or any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    user_id = get_next_user_id()  # Get the next user_id based on highest existing value

    user_data = {
        "user_id": user_id,
        "username": data["username"],
        "password": bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "gender": data.get("gender", ""),
        "nationality": data.get("nationality", ""),
        "age": int(data["age"]) if "age" in data else None,
        "weight": float(data["weight"]) if "weight" in data else None,
        "height": float(data["height"]) if "height" in data else None,
        "phone_number": data.get("phone_number", ""),
        "company_name": data.get("company_name", ""),
        "job": data.get("job", ""),
        "timestamp": datetime.utcnow()  # Use UTC time for MongoDB ISODate
    }

    try:
        if users_collection.find_one({"username": user_data["username"]}):
            return jsonify({"error": "Username already exists"}), 409

        user_id = users_collection.insert_one(user_data).inserted_id
        print("Inserted User ID:", user_id)

        return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201

    except Exception as e:
        print("Error inserting user:", str(e))
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
    

### **📌 Login & Get JWT Token**
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"message": "Login successful", "token": access_token})

### **📌 Protected Route (Requires Authentication)**
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user}, you have access!"})


### **📌 Edit User Profile (Authenticated)**
@app.route("/edit_profile", methods=["PUT"])
@jwt_required()
def edit_profile():
    current_user = get_jwt_identity()
    data = request.json

    allowed_fields = {"email", "phone_number", "job", "company_name", "weight", "height"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    users_collection.update_one({"username": current_user}, {"$set": update_data})

    return jsonify({"message": "Profile updated successfully", "updated_fields": update_data}), 200


@app.route("/get_profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = users_collection.find_one({"username": current_user}, {"_id": 0, "password": 0})  # Exclude _id & password

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200

@app.route("/get_data/user/<user_id>", methods=["GET"])
def get_data_by_user_id(user_id):
    """Retrieve all data for a given user_id from the data_collection"""
    try:
        # Query the database for documents matching the user_id
        user_data = list(data_collection.find({"user_id": int(user_id)}, {"_id": 0}))  # Exclude MongoDB `_id`

        if not user_data:
            return jsonify({"error": "No data found for this user_id"}), 404

        return jsonify({"user_id": user_id, "data": user_data}), 200

    except Exception as e:
        print("Error fetching data:", str(e))
        return jsonify({"error": "An error occurred", "details": str(e)}), 500



@app.route('/emergency_alert', methods=['POST'])
def emergency_alert():
    """
    Endpoint to check the health condition based on SpO2, BPM, and activity.
    Expects form data with 'spo2', 'bpm', and 'activity' fields.
    """
    print("Entry Endpoint Emergency Alert")
    try:
        # Get form data from the request
        data = request.json
        spo2 = data.get("spo2") # Spo2 value
        bpm = data.get("bpm") # BPM value
        activity  = data.get("activity") # Activity type (1 for walking, 2 for running)

        
       # Return the result as a JSON response
        response = {
            "text": "Emergency Alert!",
            "spo2": spo2,
            "bpm": bpm,
            "activity": activity
        }
        return jsonify(response), 200

    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid value for parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Utils
def get_next_user_id():
    """Get the next available user_id by finding the highest current value and adding 1"""
    last_user = users_collection.find_one({}, sort=[("user_id", -1)])  # Get user with highest ID
    return (last_user["user_id"] + 1) if last_user else 0  # Start at 0 if no users exist

if __name__ == "__main__":
    app.run(debug=True)