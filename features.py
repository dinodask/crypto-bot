import pandas as pd
import numpy as np
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volume import MFIIndicator
from ta.trend import ADXIndicator

FEATURE_NAMES = [
    "price_change",
    "bb_bbm",
    "bb_bbh",
    "rsi",
    "stoch",
    "macd",
    "ema_10",
    "atr",
    "obv",    
    "mfi",
    "adx",

]


def calculate_obv(df):
    obv = np.where(
        df["close"] > df["close"].shift(1),
        df["volume"],
        np.where(df["close"] < df["close"].shift(1), -df["volume"], 0),
    )
    df["obv"] = obv.cumsum()
    return df


def extract_features(df):
    df["mfi"] = MFIIndicator(
        high=df["high"], low=df["low"], close=df["close"], volume=df["volume"]
    ).money_flow_index()

    df["adx"] = ADXIndicator(
        high=df["high"], low=df["low"], close=df["close"]
    ).adx()

    df["price_change"] = df["close"].pct_change()

    bb = BollingerBands(close=df["close"])
    df["bb_bbm"] = bb.bollinger_mavg()
    df["bb_bbh"] = bb.bollinger_hband()

    df["rsi"] = RSIIndicator(close=df["close"]).rsi()
    df["stoch"] = StochasticOscillator(
        close=df["close"], high=df["high"], low=df["low"]
    ).stoch()
    df["macd"] = MACD(close=df["close"]).macd()
    df["ema_10"] = EMAIndicator(close=df["close"], window=10).ema_indicator()
    df["atr"] = AverageTrueRange(
        high=df["high"], low=df["low"], close=df["close"]
    ).average_true_range()

    df = calculate_obv(df)

    df = df.dropna()
    return df
