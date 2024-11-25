import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get the auth token from the environment variable
authToken = os.getenv("AUTH_TOKEN")

# Define the base URL of the API endpoint
url = "https://cryptopanic.com"

# Define the endpoint with the auth token
endpoint = f"/api/free/v1/posts/?auth_token={authToken}&currencies=BTC&filter=rising"

# Make the GET request
response = requests.get(url + endpoint)

# Check if the request was successful
if response.status_code == 200:
    # Process the response JSON data
    data = response.json()
    print("Data received:", data)
else:
    print("Failed to retrieve data:", response.status_code)


# convert to json
data = response.json()
#save to file
with open('data.json', 'w') as f:
    json.dump(data, f)


import matplotlib.pyplot as plt
import numpy as np

# Data for voting statistics
voting_data = [
    {"title": "Coinbase Joins Forces with the LA Clippers", "votes": {"negative": 1, "positive": 2, "important": 0, "liked": 0, "disliked": 1, "lol": 1, "toxic": 0, "saved": 0, "comments": 0}},
    {"title": "Bitcoin ETFs Set to Surpass Satoshi's Holdings by Year-End", "votes": {"negative": 0, "positive": 7, "important": 6, "liked": 7, "disliked": 0, "lol": 0, "toxic": 0, "saved": 6, "comments": 0}},
    {"title": "Hong Kong’s largest digital bank launches retail crypto trading", "votes": {"negative": 0, "positive": 5, "important": 3, "liked": 5, "disliked": 0, "lol": 0, "toxic": 0, "saved": 1, "comments": 1}},
    {"title": "Cantor Fitzgerald Joins Forces with Tether", "votes": {"negative": 0, "positive": 6, "important": 5, "liked": 6, "disliked": 0, "lol": 0, "toxic": 0, "saved": 5, "comments": 0}},
    {"title": "Solana Skyrockets: Spot ETF Filings Surge Amid Pro-Crypto Regulatory Shift!", "votes": {"negative": 3, "positive": 7, "important": 1, "liked": 6, "disliked": 2, "lol": 2, "toxic": 0, "saved": 3, "comments": 1}},
    {"title": "Highly Anticipated Spot Solana ETFs Will Be Approved in 2025", "votes": {"negative": 3, "positive": 6, "important": 4, "liked": 4, "disliked": 3, "lol": 2, "toxic": 0, "saved": 5, "comments": 3}},
    {"title": "VanEck Has Now Reiterated Its Ambitious Bitcoin Price Target Of $180,000", "votes": {"negative": 0, "positive": 7, "important": 3, "liked": 4, "disliked": 0, "lol": 0, "toxic": 0, "saved": 1, "comments": 0}},
    {"title": "Ethereum-to-bitcoin ratio plummets to three-year low as BTC approaches $100,000", "votes": {"negative": 3, "positive": 0, "important": 3, "liked": 0, "disliked": 3, "lol": 4, "toxic": 0, "saved": 0, "comments": 1}},
    {"title": "Cardano (ADA) Jumps to Top Section of Weiss Crypto Ranking", "votes": {"negative": 2, "positive": 4, "important": 4, "liked": 4, "disliked": 2, "lol": 3, "toxic": 0, "saved": 0, "comments": 0}},
    {"title": "Cardano rises 140%: Here’s why $1 could be a catalyst for FOMO and an ATH", "votes": {"negative": 5, "positive": 19, "important": 6, "liked": 13, "disliked": 5, "lol": 4, "toxic": 0, "saved": 0, "comments": 2}},
]

# Aggregating voting categories
categories = ["negative", "positive", "important", "liked", "disliked", "lol", "toxic", "saved", "comments"]
category_totals = {category: 0 for category in categories}

for item in voting_data:
    for category in categories:
        category_totals[category] += item["votes"].get(category, 0)

# Bar plot
plt.figure(figsize=(10, 6))
bars = plt.bar(category_totals.keys(), category_totals.values(), color='skyblue', edgecolor='black')

# Adding value annotations on bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2 - 0.1, yval + 0.5, int(yval), fontsize=10)

plt.title("Aggregate Voting Statistics", fontsize=14)
plt.ylabel("Vote Count", fontsize=12)
plt.xlabel("Voting Categories", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()