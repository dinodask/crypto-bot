import pandas as pd
from data_fetcher import get_klines

from binance.client import Client  # πρόσθεσε αν δεν υπάρχει ήδη

df = get_klines(
    symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, lookback="180 day ago UTC"
)


if df is None or df.empty:
    print("⚠ Δεν ελήφθησαν δεδομένα.")
else:
    df.to_csv("historical_data.csv", index=False)
    print("✅ Αποθηκεύτηκε το αρχείο historical_data.csv")
