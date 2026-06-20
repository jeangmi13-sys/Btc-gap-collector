import requests
import time
from datetime import datetime
import os

print("=== BTC Gap Collector 24/7 - Avec Retry ===")

CSV_FOLDER = "csv_data"
os.makedirs(CSV_FOLDER, exist_ok=True)

def get_binance_price():
    for attempt in range(3):
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            response = requests.get(url, timeout=15)
            return float(response.json()["price"])
        except:
            time.sleep(2)
    return None

def get_coingecko_price():
    for attempt in range(3):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url, timeout=15)
            return float(response.json()["bitcoin"]["usd"])
        except:
            time.sleep(2)
    return None

while True:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    csv_file = f"{CSV_FOLDER}/ecarts_{date_str}.csv"

    binance_price = get_binance_price()
    coingecko_price = get_coingecko_price()

    if binance_price is not None and coingecko_price is not None:
        ecart = binance_price - coingecko_price
        date_only = now.strftime("%Y-%m-%d")
        time_only = now.strftime("%H:%M:%S")

        if abs(ecart) <= 3:
            alerte = f"🚨 QUASI-ZÉRO ({int(abs(ecart))}$)"
        elif abs(ecart) <= 10:
            alerte = f"⚠️ FAIBLE ({int(abs(ecart))}$)"
        else:
            alerte = "Normal"

        if not os.path.exists(csv_file):
            with open(csv_file, "w", encoding="utf-8") as f:
                f.write("Date,Heure,Binance,CoinGecko,Ecart,Alerte\n")

        with open(csv_file, "a", encoding="utf-8") as f:
            f.write(f"{date_only},{time_only},{binance_price},{coingecko_price},{ecart:.2f},{alerte}\n")

        print(f"[{now}] Écart : {ecart:.2f} $ | Alerte : {alerte}")
    else:
        print(f"[{now}] Erreur de récupération des prix (retry en cours...)")

    time.sleep(30)
