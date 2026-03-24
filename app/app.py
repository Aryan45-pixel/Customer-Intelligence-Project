import streamlit as st
import pandas as pd
import os
import requests
import joblib
import sys

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Customer Intelligence", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
.main {
    background-color: transparent;
}
.title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #ff00cc, #3333ff);
}
</style>
""", unsafe_allow_html=True)

# ---------------- PATH FIX ----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import insert_data, fetch_data, create_user, login_user, fetch_all_data

# ---------------- RECOMMENDATION ----------------
def get_recommendation(segment, purchase, frequency):
    if segment == "High Value":
        return "🎯 Premium products + loyalty rewards"
    elif segment == "At Risk":
        return "⚠️ Give discounts to retain customer"
    elif segment == "Inactive":
        return "💤 Send offers to re-engage"
    elif segment == "Regular":
        return "🛍️ Recommend trending products"
    if purchase > 500:
        return "💎 Upsell high-value items"
    return "📊 General recommendation"

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# ================= AUTH UI (MODERN) =================
if not st.session_state["logged_in"]:

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">🔐 AI Customer Platform</div>', unsafe_allow_html=True)

    menu = st.selectbox("Select", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Signup":
        if st.button("Create Account"):
            if create_user(username, password):
                st.success("Account created! Please login.")
            else:
                st.error("User already exists")

    elif menu == "Login":
        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username

                if username == "admin":
                    st.session_state["is_admin"] = True
                else:
                    st.session_state["is_admin"] = False

                st.rerun()
            else:
                st.error("Invalid credentials")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ================= MAIN APP =================
st.sidebar.success(f"Logged in as {st.session_state['user']}")

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.session_state["is_admin"] = False
    st.rerun()

# ---------------- LOAD DATA ----------------
base = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(base, '..', 'data', 'cleaned_data.csv'))

# ---------------- TITLE ----------------
st.title("🚀 AI Customer Intelligence Platform")

# ---------------- INPUT ----------------
st.sidebar.header("Customer Input")

age = st.sidebar.slider("Age", 18, 70)
frequency = st.sidebar.slider("Previous Purchases", 1, 50)
purchase = st.sidebar.number_input("Purchase Amount", 0)

# ================= ANALYZE =================
if st.sidebar.button("Analyze Customer"):

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            params={
                "age": age,
                "frequency": frequency,
                "purchase": purchase
            }
        )

        result = response.json()

        insert_data(
            st.session_state["user"],
            age,
            frequency,
            purchase,
            result.get("segment"),
            result.get("high_spender"),
            result.get("churn")
        )

        st.subheader("🎯 Prediction Result")

        if result.get("high_spender") == 1:
            st.success("💎 High Value Customer")
        else:
            st.warning("⚠️ Low Value Customer")

        st.info(f"Segment: {result.get('segment')}")

        # 🔥 RECOMMENDATION
        st.subheader("🎯 Recommendation")
        st.success(get_recommendation(result.get("segment"), purchase, frequency))

        st.subheader("🚨 Churn Prediction")

        if result.get("churn") == 1:
            st.error("⚠️ Customer likely to churn")
        else:
            st.success("✅ Customer will stay")

        # SHAP
        st.subheader("🧠 SHAP Explanation")

        try:
            import shap
            import numpy as np

            clf = joblib.load(os.path.join(base, 'classifier.pkl'))

            input_data = pd.DataFrame(
                [[age, frequency, purchase]],
                columns=['age', 'frequency', 'monetary']
            )

            explainer = shap.TreeExplainer(clf)
            shap_values = explainer.shap_values(input_data)

            shap_vals = shap_values[-1] if isinstance(shap_values, list) else shap_values
            shap_vals = np.array(shap_vals).flatten()

            shap_df = pd.DataFrame({
                "Feature": input_data.columns,
                "Impact": shap_vals[:3]
            }).sort_values(by="Impact", ascending=False)

            st.dataframe(shap_df)
            st.bar_chart(shap_df.set_index("Feature"))

        except Exception as e:
            st.warning(f"SHAP error: {e}")

    except Exception as e:
        st.error(f"❌ API Error: {e}")

# ================= DASHBOARD =================
st.subheader("📊 Customer Intelligence Dashboard")

if st.session_state.get("is_admin", False):

    st.success("👑 Admin View")

    data = fetch_all_data()

    if data:
        df_all = pd.DataFrame(data, columns=[
            "ID", "Username", "Age", "Frequency",
            "Purchase", "Segment", "High Spender", "Churn"
        ])

        st.metric("Total Users", df_all["Username"].nunique())
        st.metric("Total Records", len(df_all))

        st.dataframe(df_all)
        st.bar_chart(df_all["Segment"].value_counts())

else:

    data = fetch_data(st.session_state["user"])

    if data:
        df_user = pd.DataFrame(data, columns=[
            "ID", "Username", "Age", "Frequency",
            "Purchase", "Segment", "High Spender", "Churn"
        ])

        st.metric("Total Records", len(df_user))
        st.dataframe(df_user)
        st.bar_chart(df_user["Segment"].value_counts())

    else:
        st.info("No data yet")
