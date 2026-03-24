import pandas as pd
import os
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'cleaned_data.csv')
APP_PATH = os.path.join(BASE_DIR, '..', 'app')

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Data loaded successfully")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

# ---------------- FEATURE ENGINEERING ----------------
df['frequency'] = df['previous_purchases']
df['monetary'] = df['purchase_amount_(usd)']
df['recency'] = df['frequency'].max() - df['frequency']

# ---------------- SEGMENTATION ----------------
rfm = df[['recency', 'frequency', 'monetary']]

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['segment'] = kmeans.fit_predict(rfm_scaled)

segment_map = {
    0: "High Value",
    1: "Regular",
    2: "At Risk",
    3: "Inactive"
}
df['segment_label'] = df['segment'].map(segment_map)

# ---------------- CLV ----------------
df['clv'] = df['monetary'] * df['frequency']

# ================= CLASSIFICATION MODEL =================
# 🔥 FIXED TARGET (IMPORTANT)
df['target'] = (
    (df['frequency'] > df['frequency'].median()) &
    (df['monetary'] > df['monetary'].median())
).astype(int)

X = df[['age', 'frequency', 'monetary']]
y = df['target']

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

print("✅ Classification model trained")

# ---------------- DEBUG ----------------
print("\n📊 Target Distribution:")
print(df['target'].value_counts())

print("\n📊 Feature Importance:")
print(clf.feature_importances_)

# ================= CHURN MODEL =================
# Simple churn logic
df['churn'] = df['frequency'].apply(lambda x: 1 if x < df['frequency'].median() else 0)

X_churn = df[['age', 'frequency', 'monetary']]
y_churn = df['churn']

churn_model = RandomForestClassifier(n_estimators=100, random_state=42)
churn_model.fit(X_churn, y_churn)

print("✅ Churn model trained")

print("\n📊 Churn Distribution:")
print(df['churn'].value_counts())

# ---------------- SAVE MODELS ----------------
try:
    joblib.dump(clf, os.path.join(APP_PATH, 'classifier.pkl'))
    joblib.dump(kmeans, os.path.join(APP_PATH, 'cluster.pkl'))
    joblib.dump(scaler, os.path.join(APP_PATH, 'scaler.pkl'))
    joblib.dump(churn_model, os.path.join(APP_PATH, 'churn_model.pkl'))

    print("✅ All models saved successfully")

except Exception as e:
    print(f"❌ Error saving models: {e}")

# ---------------- SAVE DATA ----------------
try:
    df.to_csv(DATA_PATH, index=False)
    print("✅ Cleaned data updated")

except Exception as e:
    print(f"❌ Error saving data: {e}")