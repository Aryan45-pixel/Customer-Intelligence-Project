import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../data/shopping_trends_updated.csv')

# Basic info
print("Shape:", df.shape)
print(df.head())

# Handle missing values
print(df.isnull().sum())
df = df.dropna()

# Remove duplicates
df = df.drop_duplicates()

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print(df.columns)

# Outlier check
sns.boxplot(x=df['purchase_amount_(usd)'])
plt.show()

# Feature engineering
df['spending_level'] = df['purchase_amount_(usd)'].apply(
    lambda x: 'High' if x > 500 else 'Low'
)

df['age_group'] = pd.cut(df['age'],
                        bins=[18, 25, 35, 50, 65],
                        labels=['Youth', 'Young Adult', 'Adult', 'Senior'])

# Save cleaned data
df.to_csv('../data/cleaned_data.csv', index=False)

print("✅ Data Cleaning Completed Successfully")