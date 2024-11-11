import requests
import os

# Get the auth token directly from the environment variables
authToken = os.getenv("AUTH_TOKEN")
print(authToken)

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