import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/cleaned_data.csv')

# Gender Distribution
sns.countplot(x='gender', data=df)
plt.title("Customer Distribution by Gender")
plt.show()

# Category Revenue
df.groupby('category')['purchase_amount_(usd)'].sum().sort_values().plot(kind='barh')
plt.title("Revenue by Category")
plt.show()

# Age vs Spending
sns.scatterplot(x='age', y='purchase_amount_(usd)', data=df)
plt.title("Age vs Purchase Amount")
plt.show()

# Spending Level
sns.countplot(x='spending_level', data=df)
plt.title("Spending Level Distribution")
plt.show()

# Payment Method
df.groupby('payment_method')['purchase_amount_(usd)'].sum().plot(kind='bar')
plt.title("Revenue by Payment Method")
plt.xticks(rotation=45)
plt.show()

# Frequency vs Spending
sns.boxplot(x='frequency_of_purchases', y='purchase_amount_(usd)', data=df)
plt.xticks(rotation=45)
plt.title("Frequency vs Spending")
plt.show()