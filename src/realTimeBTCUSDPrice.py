import requests
import time
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv
import threading

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenez le mot de passe MongoDB depuis les variables d'environnement
mongodb_password = os.getenv("MONGODB_PASSWORD")

uri = f"mongodb+srv://utafaro:root@cluster0.l71ap.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Créez un client MongoDB et connectez-vous au serveur
client = MongoClient(uri)
db = client["bitcoin-data"]
collection = db["prices"]

# Fonction pour récupérer et insérer les données dans MongoDB
def fetch_and_store_data():
    url = "https://api.binance.com"
    symbol = "BTCUSDT"
    interval = "1d"  # Intervalle de 1 jour pour obtenir des données journalières

    # Calculer la période des 3 derniers mois
    end_time = int(time.time() * 1000)  # Temps actuel en millisecondes
    start_time = int((time.time() - 3 * 30 * 24 * 60 * 60) * 1000)  # 3 mois avant

    # Construire l'endpoint avec la période spécifiée
    endpoint = f"/api/v3/klines?symbol={symbol}&interval={interval}&startTime={start_time}&endTime={end_time}"

    # Récupérer les données de l'API Binance
    response = requests.get(url + endpoint)
    
    if response.status_code == 200:
        data = response.json()
        
        for item in data:
            timestamp = item[0] / 1000  # Convertir en secondes
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            open_price = item[1]
            high_price = item[2]
            low_price = item[3]
            close_price = item[4]
            
            # Créer un dictionnaire avec les données du prix
            price_data = {
                "date": date,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price
            }

            # Insérer les données dans MongoDB
            collection.insert_one(price_data)
            
    else:
        print("Échec de la récupération des données:", response.status_code)

# Fonction pour écouter les changements dans MongoDB avec Change Streams
def listen_for_changes():
    # Assurez-vous que Change Streams fonctionne (MongoDB Replica Set requis)
    try:
        with collection.watch() as stream:
            print("Écoute des changements en temps réel...")
            for change in stream:
                print("Changement détecté:", change)
                # Vous pouvez effectuer d'autres actions ici si vous le souhaitez (par exemple, traiter les données)
    except ConnectionFailure:
        print("Échec de la connexion à MongoDB. Assurez-vous que MongoDB est en mode Replica Set.")

# Fonction principale qui combine l'insertion des données et l'écoute des changements
def main():
    try:
        # Démarrer un fil d'exécution pour écouter les changements en parallèle
        threading.Thread(target=listen_for_changes, daemon=True).start()

        # Récupérer et insérer les données des 3 derniers mois
        fetch_and_store_data()  # Récupérer les données et les insérer dans MongoDB

            

    except KeyboardInterrupt:
        print("Arrêt du script.")

if __name__ == "__main__":
    main()
