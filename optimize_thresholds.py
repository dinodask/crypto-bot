import subprocess
import re
import pandas as pd
import shutil
import os

# Αποθηκεύουμε το αρχικό config.py
shutil.copyfile("config.py", "config_backup.py")

buy_values = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
sell_values = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

results = []

try:
    for buy in buy_values:
        for sell in sell_values:
            if sell >= buy:
                continue

            # Τροποποιούμε το config.py
            with open("config.py", "r", encoding="utf-8") as f:
                lines = f.readlines()

            with open("config.py", "w", encoding="utf-8") as f:
                for line in lines:
                    if line.strip().startswith("BUY_THRESHOLD"):
                        f.write(f"BUY_THRESHOLD = {buy}\n")
                    elif line.strip().startswith("SELL_THRESHOLD"):
                        f.write(f"SELL_THRESHOLD = {sell}\n")
                    else:
                        f.write(line)

            print(f"🔍 Testing BUY={buy}, SELL={sell}...")

            # Τρέχουμε το backtest.py
            process = subprocess.Popen(
                ["python", "backtest.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            output, _ = process.communicate()

            try:
                final_value = float(
                    re.search(r"Τελική αξία χαρτοφυλακίου:\s+([0-9.]+)", output).group(1)
                )
                profit = float(
                    re.search(r"Κέρδος/Ζημιά:\s+([0-9.]+)", output).group(1)
                )
                roi = float(
                    re.search(r"ROI:\s+([0-9.]+)", output).group(1)
                )
                trades = int(
                    re.search(r"Πλήθος trades:\s+([0-9]+)", output).group(1)
                )
            except Exception as e:
                print("❌ Σφάλμα στην ανάλυση αποτελεσμάτων:", e)
                continue

            print(f"✅ ROI={roi:.2f}%, Trades={trades}")

            results.append({
                "BUY": buy,
                "SELL": sell,
                "Final Value": final_value,
                "Profit": profit,
                "ROI": roi,
                "Trades": trades,
            })

    # Επιλογή του καλύτερου συνδυασμού
    df = pd.DataFrame(results)
    df.to_csv("threshold_results.csv", index=False)
    best_row = df.loc[df["ROI"].idxmax()]

    # Γράφουμε τις καλύτερες ρυθμίσεις στο config.py
    with open("config_backup.py", "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open("config.py", "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip().startswith("BUY_THRESHOLD"):
                f.write(f"BUY_THRESHOLD = {best_row['BUY']}\n")
            elif line.strip().startswith("SELL_THRESHOLD"):
                f.write(f"SELL_THRESHOLD = {best_row['SELL']}\n")
            else:
                f.write(line)

    print("\n🏁 Βέλτιστες Ρυθμίσεις:")
    print(f"   BUY_THRESHOLD = {best_row['BUY']}")
    print(f"   SELL_THRESHOLD = {best_row['SELL']}")
    print(f"   ROI = {best_row['ROI']:.2f}%")
    print("🎉 Το config.py ενημερώθηκε με τις καλύτερες τιμές.")

finally:
    # Σβήνουμε το προσωρινό backup
    if os.path.exists("config_backup.py"):
        os.remove("config_backup.py")
