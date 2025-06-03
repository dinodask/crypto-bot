from features import extract_features, FEATURE_NAMES
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
import joblib

# Φόρτωση και προετοιμασία δεδομένων
df = pd.read_csv("historical_data.csv")
df = extract_features(df)

X = df[FEATURE_NAMES].iloc[:-1]
y = np.where(df["close"].shift(-1) > df["close"], 1, 0)[:-1]

# Διαχωρισμός σε εκπαίδευση και τεστ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Κανονικοποίηση
scaler = joblib.load("scaler.pkl")
X_test_scaled = scaler.transform(X_test)

# Φόρτωση μοντέλου
model = joblib.load("model.pkl")

# Πρόβλεψη
y_pred = model.predict(X_test_scaled)

# Αξιολόγηση
print("🔍 Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("🎯 Precision:", round(precision_score(y_test, y_pred), 4))
print("📢 Recall:", round(recall_score(y_test, y_pred), 4))
print("\n📊 Αναλυτικό report:\n", classification_report(y_test, y_pred, digits=4))
