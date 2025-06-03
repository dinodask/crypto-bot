@echo off
cd /d "C:\Users\dinod\Desktop\crypto-bot"

REM Εκκίνηση του bot (main.py) σε ξεχωριστό minimized παράθυρο
start /min cmd /c "python main.py"

REM Περιμένει 5 δευτερόλεπτα και ξεκινά το dashboard
timeout /t 5 > nul
start /min cmd /c "python dashboard.py"

echo ✅ Το Crypto Bot ξεκίνησε επιτυχώς.
pause
