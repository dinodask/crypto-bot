from trader import Trader
import schedule
import time
import config


def run_bot():
    if config.LIVE_MODE:
        confirm = (
            input("⚠️ Το bot είναι σε LIVE MODE. Θες να συνεχίσει; (yes/όχι): ")
            .strip()
            .lower()
        )
        if confirm not in ["yes", "y", "ναι"]:
            print("⛔ Εκτέλεση ακυρώθηκε.")
            return

    bot = Trader()
    bot.run_once()  # υποθέτουμε ότι δεν έχει εσωτερικό loop


# Υπολογίζουμε λεπτά από INTERVAL_SECONDS
interval_minutes = config.INTERVAL_SECONDS // 60
print(f"📆 Το bot είναι ενεργό και θα τρέχει κάθε {interval_minutes} λεπτά.\n")

# Προγραμματισμός με βάση το INTERVAL_SECONDS
schedule.every(interval_minutes).minutes.do(run_bot)

# Εκτελείται μία φορά άμεσα
run_bot()

# Loop scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
