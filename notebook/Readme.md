1. Customers aged 25–35 contribute highest revenue
2. Electronics and Clothing are top-selling categories
3. High-value customers are limited but generate major revenue
4. Credit card users spend more than other payment methods
5. Frequent buyers show higher purchase amounts

# 🚀 AI Customer Intelligence Platform

An end-to-end **AI-powered customer analytics platform** that helps businesses understand customer behavior, predict churn, segment users, and generate smart recommendations.

---

## 🎯 Project Objective

The goal of this project is to **leverage machine learning and data analytics** to:

* Understand customer purchasing behavior
* Identify high-value customers
* Predict churn risk
* Provide personalized recommendations
* Help businesses improve retention and revenue

---

## 🧠 Key Features

### 🔹 Customer Segmentation

* Uses clustering (KMeans) to divide customers into:

  * 💎 High Value
  * 👤 Regular
  * ⚠️ At Risk
  * 💤 Inactive

---

### 🔹 High Spender Prediction

* Machine learning model predicts whether a customer is a **high spender or not**

---

### 🔹 Churn Prediction 🚨

* Identifies customers likely to leave
* Helps in taking preventive actions (discounts, offers)

---

### 🔹 Recommendation System 🎯

* Suggests actions based on customer segment:

  * Premium offers
  * Discounts
  * Re-engagement campaigns

---

### 🔹 Interactive Dashboard 📊

* Built using Streamlit
* Visualizes:

  * Customer segments
  * Revenue trends
  * CLV (Customer Lifetime Value)

---

### 🔹 Authentication System 🔐

* Login / Signup functionality
* User-specific data tracking
* Admin dashboard support

---

## 🏗️ Tech Stack

| Layer         | Technology   |
| ------------- | ------------ |
| Frontend      | Streamlit    |
| Backend       | FastAPI      |
| ML Models     | Scikit-learn |
| Database      | SQLite       |
| Visualization | Matplotlib   |

---

## 📂 Project Structure

```
customer-intelligence-project/
│
├── app/                # Streamlit frontend
│   └── app.py
│
├── api/                # FastAPI backend
│   └── main.py
│
├── data/               # Dataset
│   └── cleaned_data.csv
│
├── models/             # ML & NLP models
│   ├── classifier.pkl
│   ├── cluster.pkl
│   └── scaler.pkl
│
├── src/
│   └── database.py     # Database logic
│
└── README.md
```

---

## ⚙️ How to Run the Project

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/customer-intelligence-project.git
cd customer-intelligence-project
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv .venv
.\.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Run Backend (FastAPI)

```
uvicorn api.main:app --reload
```

---

### 5️⃣ Run Frontend (Streamlit)

```
streamlit run app/app.py
```

---

### 6️⃣ Open in Browser

```
http://localhost:8501
```

---

## 📊 Example Use Cases

* E-commerce platforms (Amazon, Flipkart)
* Food delivery apps (Swiggy, Zomato)
* Retail businesses
* Subscription-based services

---

## 💡 Future Enhancements

* 🔐 JWT Authentication
* ☁️ Cloud Deployment (AWS / Render)
* 📈 Advanced dashboards (Plotly / Power BI style)
* 🤖 Real-time prediction system
* 📦 Docker containerization

---

## 🧑‍💻 Author

**Aryan Todkar**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share it!

---
