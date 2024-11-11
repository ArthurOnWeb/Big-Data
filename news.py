import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the auth token from the environment variable
authToken = os.getenv("AUTH_TOKEN")

# Define the base URL of the API endpoint
url = "https://cryptopanic.com"

# Define the endpoint with the auth token
endpoint = f"/api/free/v1/posts/?auth_token={authToken}"

# Make the GET request
response = requests.get(url + endpoint)

# Check if the request was successful
if response.status_code == 200:
    # Process the response JSON data
    data = response.json()
    print("Data received:", data)
else:
    print("Failed to retrieve data:", response.status_code)
