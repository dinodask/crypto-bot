import pandas as pd
from binance.client import Client
import os

# Προαιρετικά: Ορίζει API keys μέσω περιβάλλοντος ή σκληρά
api_key = os.getenv("BINANCE_API_KEY", "")  # ή βάλε κατευθείαν π.χ. "ABCD123..."
api_secret = os.getenv("BINANCE_API_SECRET", "")
client = Client(api_key, api_secret)

def get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, lookback="7 day ago UTC"):
    print("✅ Η get_klines() τραβά δεδομένα από Binance για 7 μέρες")

    # Παίρνει ιστορικά δεδομένα από Binance
    klines = client.get_historical_klines(symbol, interval, lookback)

    # Φτιάχνει DataFrame
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    # Καθάρισμα δεδομένων
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    return df[["timestamp", "close", "volume"]]
