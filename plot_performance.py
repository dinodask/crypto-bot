import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def plot(save_to_file=False):
    try:
        df = pd.read_csv(
            "bot_run_log.csv",
            header=None,
            names=[
                "timestamp",
                "prediction",
                "action",
                "price",
                "balance_usdt",
                "balance_asset",
            ],
        )
    except FileNotFoundError:
        print("⛔ Δεν βρέθηκε το αρχείο bot_run_log.csv")
        return

    df = df[
        df["timestamp"] != "timestamp"
    ]  # Αφαίρεσε γραμμές όπου 'timestamp' είναι η ίδια η λέξη
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])  # Πετάμε γραμμές με λάθος ημερομηνία
    df["balance_asset"] = pd.to_numeric(df["balance_asset"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["balance_asset", "price"])
    df["prediction"] = pd.to_numeric(df["prediction"], errors="coerce")

    df["asset_value"] = df["balance_asset"] * df["price"]
    df["balance_usdt"] = pd.to_numeric(df["balance_usdt"], errors="coerce")

    df["total_value"] = df["balance_usdt"] + df["asset_value"]

    start_date = df["timestamp"].min().strftime("%Y-%m-%d")
    end_date = df["timestamp"].max().strftime("%Y-%m-%d")
    plot_title = f" Bot Portfolio από {start_date} έως {end_date}"

    buy_df = df[df["action"] == "BUY"]
    sell_df = df[df["action"] == "SELL"]

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["total_value"], label="Συνολική Αξία", linewidth=2)
    plt.plot(df["timestamp"], df["balance_usdt"], label="USDT", linestyle="--")
    plt.plot(df["timestamp"], df["asset_value"], label="BTC (σε USDT)", linestyle="--")

    plt.scatter(
        buy_df["timestamp"],
        buy_df["total_value"],
        color="green",
        label="BUY",
        marker="^",
        zorder=5,
    )
    plt.scatter(
        sell_df["timestamp"],
        sell_df["total_value"],
        color="red",
        label="SELL",
        marker="v",
        zorder=5,
    )

    def add_prediction_zone(df, condition, color, label):
        in_zone = False
        start = None
        for i in range(len(df)):
            if condition(df.iloc[i]):
                if not in_zone:
                    start = df.iloc[i]["timestamp"]
                    in_zone = True
            else:
                if in_zone:
                    end = df.iloc[i]["timestamp"]
                    plt.axvspan(
                        start,
                        end,
                        color=color,
                        alpha=0.1,
                        label=label if start == df.iloc[0]["timestamp"] else "",
                    )
                    in_zone = False
        if in_zone:
            end = df.iloc[-1]["timestamp"]
            plt.axvspan(
                start,
                end,
                color=color,
                alpha=0.1,
                label=label if start == df.iloc[0]["timestamp"] else "",
            )

    add_prediction_zone(df, lambda row: row["prediction"] >= 0.7, "green", "LONG ZONE")
    add_prediction_zone(df, lambda row: row["prediction"] <= 0.3, "red", "SHORT ZONE")

    plt.title(plot_title)
    plt.xlabel("Χρόνος")
    plt.ylabel("Αξία σε USDT")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_to_file:
        filename = f"bot_portfolio_{start_date}_to_{end_date}.png"
        plt.savefig(filename)
        print(f" Το γράφημα αποθηκεύτηκε ως {filename}")

    plt.show()


if __name__ == "__main__":
    plot(save_to_file=True)
