import os
import csv
import time
import pandas as pd
import numpy as np
from datetime import datetime
from config import LIVE_MODE, BUY_THRESHOLD, SELL_THRESHOLD
from data_fetcher import get_klines
from features import extract_features, FEATURE_NAMES
import joblib
from sklearn.model_selection import cross_val_score
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

class Trader:
    def __init__(self):
        self.model = joblib.load("model.pkl")
        self.scaler = joblib.load("scaler.pkl")
        self.usdt_balance = 1000
        self.btc_balance = 0
        self.feature_names = FEATURE_NAMES
        self.last_buy_price = None
        self.last_atr = None

    def log_trade(self, prob_up, action, price):
        log_exists = os.path.isfile("bot_run_log.csv")
        with open("bot_run_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not log_exists:
                writer.writerow(
                    ["timestamp", "prediction", "action", "price", "usdt_balance", "btc_balance"]
                )
            writer.writerow(
                [
                    datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    round(prob_up, 4),
                    action,
                    price,
                    round(self.usdt_balance, 2),
                    round(self.btc_balance, 6),
                ]
            )

    def log_to_trade_log(self, action, price):
        log_exists = os.path.isfile("trade_log.csv")
        with open("trade_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not log_exists:
                writer.writerow(["timestamp", "action", "price", "amount", "balance_usdt", "balance_asset"])
            writer.writerow([
                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                action,
                round(price, 2),
                round(self.btc_balance if action == "BUY" else self.btc_balance, 6),
                round(self.usdt_balance, 2),
                round(self.btc_balance, 6)
            ])

    def run_once(self, price, timestamp=None):
        now = timestamp or datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Αν έχεις μόνο USDT → αγόρασε BTC
        if self.usdt_balance > 0 and self.btc_balance == 0:
            self.btc_balance = self.usdt_balance / price
            self.last_buy_price = price
            self.usdt_balance = 0
            print(f"[{now}] 🟢 BUY | Τιμή: {price:.2f} | BTC: {self.btc_balance:.6f}")
            return "BUY"

        # Αν έχεις BTC → έλεγξε για κέρδος
        if self.btc_balance > 0:
            increase = (price - self.last_buy_price) / self.last_buy_price
            if increase >= 0.02:
                value_now = self.btc_balance * price
                value_then = self.btc_balance * self.last_buy_price
                profit = value_now - value_then

                btc_to_sell = profit / price
                self.usdt_balance += profit
                self.btc_balance -= btc_to_sell

                print(f"[{now}] 🟡 SELL PROFIT | Τιμή: {price:.2f} | Πούλησε: {btc_to_sell:.6f} BTC | Νέο BTC: {self.btc_balance:.6f} | USDT: {self.usdt_balance:.2f}")
                return "SELL PROFIT"

        print(f"[{now}] 🔵 HOLD | Τιμή: {price:.2f} | BTC: {self.btc_balance:.6f} | USDT: {self.usdt_balance:.2f}")
        return "HOLD"


if __name__ == "__main__":
    trader = Trader()
    trader.run_once()
    # trader.run_loop()
