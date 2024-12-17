from pymongo import MongoClient

from dotenv import load_dotenv
import os
import json
from pymongo.mongo_client import MongoClient

# Load environment variables from .env file
load_dotenv()



# Get the auth token from the environment variable
mongodb_password = os.getenv("MONGODB_PASSWORD")


uri = f"mongodb+srv://utafaro:root@cluster0.l71ap.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Get the database
db = client["bitcoin-data"]
collection = db["news"]

# Insert a json file by read data.json
with open('data.json') as f:
    data = json.load(f)

insert = collection.insert_one(data)



print("Data inserted with ID:", insert.inserted_id)
client.close()
