import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('../data/laptop_data.csv')

print("="*50)
print("LAPTOP PRICE PREDICTION - DATA EXPLORATION")
print("="*50)

# 1. Dataset Overview
print("\n1. DATASET OVERVIEW")
print("-"*50)
print(f"Dataset Shape: {df.shape}")
print(f"\nColumn Names and Types:")
print(df.dtypes)
print(f"\nFirst 5 rows:")
print(df.head())

# 2. Missing Values
print("\n2. MISSING VALUES CHECK")
print("-"*50)
print(df.isnull().sum())

# 3. Statistical Summary
print("\n3. STATISTICAL SUMMARY")
print("-"*50)
print(df.describe())

# 4. Price Distribution
print("\n4. PRICE ANALYSIS")
print("-"*50)
print(f"Mean Price: ${df['Price'].mean():.2f}")
print(f"Median Price: ${df['Price'].median():.2f}")
print(f"Min Price: ${df['Price'].min():.2f}")
print(f"Max Price: ${df['Price'].max():.2f}")
print(f"Price Range: ${df['Price'].max() - df['Price'].min():.2f}")

# 5. Brand Analysis
print("\n5. BRAND ANALYSIS")
print("-"*50)
print(df.groupby('Brand')['Price'].agg(['mean', 'count']).sort_values('mean', ascending=False))

# 6. Processor Analysis
print("\n6. PROCESSOR ANALYSIS")
print("-"*50)
print(df.groupby('Processor')['Price'].mean().sort_values(ascending=False))

# 7. RAM Analysis
print("\n7. RAM ANALYSIS")
print("-"*50)
print(df.groupby('RAM_GB')['Price'].mean().sort_values(ascending=False))

# 8. GPU Analysis
print("\n8. GPU ANALYSIS")
print("-"*50)
print(df.groupby('GPU')['Price'].mean().sort_values(ascending=False))

# 9. Correlation Analysis
print("\n9. CORRELATION ANALYSIS")
print("-"*50)
numeric_cols = df.select_dtypes(include=[np.number]).columns
print(df[numeric_cols].corr()['Price'].sort_values(ascending=False))

print("\n" + "="*50)
print("DATA EXPLORATION COMPLETED")
print("="*50)
