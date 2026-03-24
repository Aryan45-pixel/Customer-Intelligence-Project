from fastapi import FastAPI
import joblib
import os

app = FastAPI(title="Customer Intelligence API")

# ---------------- PATH SETUP ----------------
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, '..', 'app')

# ---------------- LOAD MODELS ----------------
try:
    clf = joblib.load(os.path.join(model_path, 'classifier.pkl'))
    kmeans = joblib.load(os.path.join(model_path, 'cluster.pkl'))
    scaler = joblib.load(os.path.join(model_path, 'scaler.pkl'))
    churn_model = joblib.load(os.path.join(model_path, 'churn_model.pkl'))

    print("✅ All models loaded successfully")

except Exception as e:
    print(f"❌ Error loading models: {e}")

# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "🚀 API is running"}

# ---------------- PREDICTION ----------------
@app.post("/predict")
def predict(age: int, frequency: int, purchase: float):

    try:
        # ---------------- CLASSIFICATION ----------------
        pred = clf.predict([[age, frequency, purchase]])

        # ---------------- SEGMENTATION ----------------
        rfm_input = scaler.transform([[50 - frequency, frequency, purchase]])
        seg = kmeans.predict(rfm_input)

        segment_map = {
            0: "High Value",
            1: "Regular",
            2: "At Risk",
            3: "Inactive"
        }

        # ---------------- CHURN PREDICTION ----------------
        churn_pred = churn_model.predict([[age, frequency, purchase]])

        # ---------------- RESPONSE ----------------
        return {
            "high_spender": int(pred[0]),
            "segment": segment_map[seg[0]],
            "churn": int(churn_pred[0])
        }

    except Exception as e:
        return {"error": str(e)}