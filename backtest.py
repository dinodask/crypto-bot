from trader import Trader
from data_fetcher import get_klines
print("✅ backtest.py χρησιμοποιεί get_klines από data_fetcher")
df = get_klines()
print(f"🔢 Πλήθος γραμμών που επέστρεψε: {len(df)}")

from features import extract_features
import csv

def run_backtest():
    print("✅ Η get_klines() τραβά δεδομένα από Binance για 7 μέρες")
    df = get_klines(lookback="7 day ago UTC")
    df = extract_features(df)

    trader = Trader()

    with open("backtest_log.csv", mode="w", newline="") as log_file:
        writer = csv.DictWriter(log_file, fieldnames=["timestamp", "action", "price", "usdt", "btc"])
        writer.writeheader()
        trader = Trader()  # ✅ Μία φορά, έξω από το for loop
        for i in range(len(df)):
            price = df["close"].iloc[i]
            timestamp = df["timestamp"].iloc[i]
            action = trader.run_once(price, timestamp)

            writer.writerow({
                "timestamp": timestamp,
                "action": action,
                "price": round(price, 2),
                "usdt": round(trader.usdt_balance, 2),
                "btc": round(trader.btc_balance, 6)
            })

    print("\n✅ Backtest complete. Results saved to backtest_log.csv")
import pandas as pd

# Ανάλυση αρχείου αποτελεσμάτων
df = pd.read_csv("backtest_log.csv")
df["total_value"] = df["usdt"] + df["btc"] * df["price"]

initial = df["total_value"].iloc[0]
final = df["total_value"].iloc[-1]
profit = final - initial
percent = (profit / initial) * 100

counts = df["action"].value_counts()
print("\\n✅ Backtest Complete")
print(f"📊 Τελική Αξία: {final:.2f} USDT")
print(f"💰 Καθαρό Κέρδος: {profit:.2f} USDT ({percent:.2f}%)")
print(f"🟢 Αγορές: {counts.get('BUY', 0)} | 🟡 Πωλήσεις: {counts.get('SELL PROFIT', 0)} | 🔵 HOLD: {counts.get('HOLD', 0)}")
