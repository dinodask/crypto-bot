import pandas as pd
import matplotlib.pyplot as plt


def analyze():
    log_file = "bot_run_log.csv"
    trade_file = "trade_log.csv"

    try:
        log_df = pd.read_csv(
            log_file,
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

    try:
        trade_df = pd.read_csv(trade_file)
    except FileNotFoundError:
        trade_df = pd.DataFrame(
            columns=[
                "timestamp",
                "action",
                "price",
                "amount",
                "balance_usdt",
                "balance_asset",
            ]
        )

    total_runs = len(log_df)
    buys = log_df["action"].value_counts().get("BUY", 0)
    sells = log_df["action"].value_counts().get("SELL", 0)
    stop_loss = log_df["action"].value_counts().get("STOP LOSS SELL", 0)
    take_profit = log_df["action"].value_counts().get("TAKE PROFIT SELL", 0)

    start_usdt = 1000
    final_usdt = float(log_df.iloc[-1]["balance_usdt"])
    final_btc = float(log_df.iloc[-1]["balance_asset"])
    final_price = float(log_df.iloc[-1]["price"])
    total_value = final_usdt + (final_btc * final_price)

    roi = ((total_value - start_usdt) / start_usdt) * 100

    # KPIs από trade_log
    num_trades = len(trade_df) // 2  # υποθέτουμε buy/sell ζεύγη
    trade_returns = []
    wins = 0

    for i in range(0, len(trade_df) - 1, 2):
        buy = trade_df.iloc[i]
        sell = trade_df.iloc[i + 1]
        if buy["action"] == "BUY" and sell["action"] in [
            "SELL",
            "STOP LOSS SELL",
            "TAKE PROFIT SELL",
        ]:
            ret = (sell["price"] - buy["price"]) / buy["price"]
            trade_returns.append(ret)
            if ret > 0:
                wins += 1

    avg_return = (sum(trade_returns) / len(trade_returns)) * 100 if trade_returns else 0
    win_rate = (wins / len(trade_returns)) * 100 if trade_returns else 0

    print("📊 ΑΞΙΟΛΟΓΗΣΗ BOT")
    print(f"   - Συνολικά runs: {total_runs}")
    print(f"   - Αγορές: {buys} | Πωλήσεις: {sells}")
    print(f"   - Take Profit: {take_profit} | Stop Loss: {stop_loss}")
    print(f"   - Τελική αξία χαρτοφυλακίου: {total_value:.2f} USDT")
    print(f"   - ROI: {roi:.2f}%")
    print(f"   - Μέση απόδοση ανα trade: {avg_return:.2f}%")
    print(f"   - Ποσοστό επιτυχημένων trades: {win_rate:.2f}%")
    print("")

    # Οπτική αναπαράσταση
    log_df = log_df[log_df["timestamp"] != "timestamp"]
    log_df["timestamp"] = pd.to_datetime(log_df["timestamp"], errors="coerce")
    log_df["balance_usdt"] = pd.to_numeric(log_df["balance_usdt"], errors="coerce")
    log_df["balance_asset"] = pd.to_numeric(log_df["balance_asset"], errors="coerce")
    log_df["price"] = pd.to_numeric(log_df["price"], errors="coerce")

    log_df.set_index("timestamp", inplace=True)
    log_df["portfolio_value"] = log_df["balance_usdt"] + (
        log_df["balance_asset"] * log_df["price"]
    )

    plt.figure(figsize=(12, 6))
    plt.plot(log_df.index, log_df["portfolio_value"], label="Portfolio Value")
    plt.title(" Portfolio Value Over Time")
    plt.xlabel("Time")
    plt.ylabel("USDT")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analyze()
