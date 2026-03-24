import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Sample dataset (you can expand later)
data = {
    "review": [
        "great product", "bad quality", "excellent service",
        "not good", "very happy", "worst experience"
    ],
    "sentiment": [1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['review'])
y = df['sentiment']

model = MultinomialNB()
model.fit(X, y)

joblib.dump(model, '../models/sentiment.pkl')
joblib.dump(vectorizer, '../models/vectorizer.pkl')

print("✅ NLP model saved")