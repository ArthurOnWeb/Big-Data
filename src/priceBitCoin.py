import requests
import time
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd

# Endpoint Binance pour les informations de la paire BTC/USDT
url_binance = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
# Endpoint Blockchain pour récupérer le Hash Rate
url_blockchain = "https://api.blockchain.info/charts/hash-rate?timespan=30days&format=json"

# Nom du fichier CSV pour sauvegarder les données
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
csv_file = DATA_DIR / "bitcoin_prices_volume_rsi_ma50_hashrate.csv"

# Périodes pour le calcul des indicateurs
RSI_PERIOD = 14
MA_PERIOD = 50

# Création de l'en-tête du fichier CSV
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "price", "volume", "RSI", "MA_50", "hash_rate"])

print("Début de la collecte des prix Bitcoin, volumes, RSI, MA_50 et Hash Rate (toutes les 10 secondes)...")

# Liste pour stocker les prix et calculer les indicateurs
price_list = []

# Fonction pour calculer le RSI
def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return None  # Pas assez de données pour calculer le RSI
    
    df = pd.DataFrame(prices, columns=["Close"])
    delta = df["Close"].diff()
    
    gain = delta.where(delta > 0, 0)  # Gains positifs
    loss = -delta.where(delta < 0, 0)  # Pertes négatives
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.iloc[-1]  # Dernière valeur RSI

# Fonction pour calculer la MA_50 (Moyenne mobile à 50 périodes)
def calculate_ma(prices, period=50):
    if len(prices) < period:
        return None  # Pas assez de données pour calculer la MA_50
    return sum(prices[-period:]) / period  # Moyenne des 50 derniers prix

# Fonction pour récupérer le Hash Rate
def get_hash_rate():
    response = requests.get(url_blockchain)
    data = response.json()
    # Récupérer le dernier hash rate du JSON
    hash_rate = data["values"][-1]["y"]  # Dernière valeur de hash rate en TH/s
    return hash_rate

# Boucle pour récupérer les prix et volumes toutes les 10 secondes
try:
    start_time = time.time()
    while time.time() - start_time < 86400:  # 86400 secondes = 1 jour
        # Appel de l'API Binance
        response_binance = requests.get(url_binance)
        data_binance = response_binance.json()

        # Récupération du prix et du volume d'échange
        price = float(data_binance["lastPrice"])  # Dernier prix du BTC/USDT
        volume = data_binance["volume"]           # Volume total des dernières 24 heures
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ajouter le prix à la liste pour calculer le RSI et MA_50
        price_list.append(price)

        # Calcul du RSI
        rsi = calculate_rsi(price_list, RSI_PERIOD)

        # Calcul de la MA_50
        ma_50 = calculate_ma(price_list, MA_PERIOD)

        # Récupérer le Hash Rate actuel
        hash_rate = get_hash_rate()

        # Sauvegarde des données dans le fichier CSV
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, price, volume, rsi, ma_50, hash_rate])

        print(f"{timestamp} | Prix : {price} | Volume : {volume} | RSI : {rsi} | MA_50 : {ma_50} | Hash Rate : {hash_rate} TH/s")

        # Attente de 10 secondes
        time.sleep(10)

except KeyboardInterrupt:
    print("Collecte interrompue manuellement.")
except Exception as e:
    print(f"Erreur : {e}")

print("Collecte des données terminée.")
