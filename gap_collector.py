import requests
import time
from datetime import datetime
import os

print("=== BTC Gap Collector 24/7 - Format compatible Tableur ===")

CSV_FOLDER = "csv_data"
os.makedirs(CSV_FOLDER, exist_ok=True)

def get_binance_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=10)
        return float(response.json()["price"])
    except:
        return None

def get_coingecko_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        return float(response.json()["bitcoin"]["usd"])
    except:
        return None

while True:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    csv_file = f"{CSV_FOLDER}/ecarts_{date_str}.csv"

    binance_price = get_binance_price()
    coingecko_price = get_coingecko_price()

    if binance_price is not None and coingecko_price is not None:
        ecart = binance_price - coingecko_price
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        date_only = now.strftime("%Y-%m-%d")
        time_only = now.strftime("%H:%M:%S")

        # Alerte (comme dans ton ancien script)
        if abs(ecart) <= 3:
            alerte = f"🚨 QUASI-ZÉRO ({int(abs(ecart))}$)"
        elif abs(ecart) <= 10:
            alerte = f"⚠️ FAIBLE ({int(abs(ecart))}$)"
        else:
            alerte = "Normal"

        # Création du fichier avec en-tête si besoin
        if not os.path.exists(csv_file):
            with open(csv_file, "w", encoding="utf-8") as f:
                f.write("Date,Heure,Binance,CoinGecko,Ecart,Alerte\n")

        with open(csv_file, "a", encoding="utf-8") as f:
            f.write(f"{date_only},{time_only},{binance_price},{coingecko_price},{ecart:.2f},{alerte}\n")

        print(f"[{timestamp}] Écart : {ecart:.2f} $ | Alerte : {alerte}")
    else:
        print(f"[{now}] Erreur de récupération des prix")

    time.sleep(30)  # 30 secondes
