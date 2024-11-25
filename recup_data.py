from pymongo import MongoClient

from dotenv import load_dotenv
import os

from pymongo.mongo_client import MongoClient

# Load environment variables from .env file
load_dotenv()



# Get the auth token from the environment variable
mongodb_password = os.getenv("MONGODB_PASSWORD")


uri = f"mongodb+srv://utafaro:root@cluster0.9ousx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Get the database
db = client["bitcoin-data"]
collection = db["price"]

document = {"priceClose": 50000}
insert = collection.insert_one(document)
print("Data inserted with ID:", insert.inserted_id)
client.close()
