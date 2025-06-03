import pandas as pd
import joblib
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from features import extract_features, FEATURE_NAMES  # ✅ σωστά import

# 📥 Φόρτωση ιστορικών δεδομένων
df = pd.read_csv("historical_data.csv")
df = extract_features(df)  # ✅ μοναδική εξαγωγή χαρακτηριστικών

# 🎯 Ορισμός χαρακτηριστικών και labels
features = FEATURE_NAMES
df["label"] = (df["close"].shift(-1) > df["close"]).astype(int)
df = df.dropna()

X = df[features]
y = df["label"]

# ⚖️ Κανονικοποίηση
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 🧠 Εκπαίδευση μοντέλου
model = LGBMClassifier()
model.fit(pd.DataFrame(X_scaled, columns=features), y)

# 💾 Αποθήκευση μοντέλου και scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("✅ Μοντέλο και scaler αποθηκεύτηκαν.")
