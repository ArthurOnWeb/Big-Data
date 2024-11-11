"""
We can get the price of Bitcoin during this second
https://developers.binance.com/docs/binance-spot-api-docs/rest-api/public-api-endpoints#kline-intervals
"""
import requests

# Define the base URL of the API endpoint
url = "https://api.binance.com"

# Define the endpoint with the correct symbol format
endpoint = "/api/v3/klines?symbol=BTCUSDT&interval=1s&limit=1"

# Make the GET request
response = requests.get(url + endpoint)

# Check if the request was successful
if response.status_code == 200:
    # Process the response JSON data
    data = response.json()
    print("Data received:", data)
else:
    print("Failed to retrieve data:", response.status_code)