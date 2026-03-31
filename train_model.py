import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("LAPTOP PRICE PREDICTION - MODEL TRAINING (INR)")
print("="*60)

df = pd.read_csv('data/laptop_data.csv')
print(f"\nDataset loaded: {df.shape}")

# Encode categoricals
label_encoders = {}
categorical_cols = ['Brand', 'Processor', 'Generation', 'Storage_Type', 'GPU', 'OS']

for col in categorical_cols:
    le = LabelEncoder()
    df[col + '_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# Engineered features
df['Storage_RAM_Ratio'] = df['Storage_GB'] / df['RAM_GB']
df['Is_Gaming'] = ((df['GPU'] != 'Integrated') & (df['RAM_GB'] >= 16)).astype(int)
df['Is_Premium'] = (df['Brand'].isin(['Apple', 'Microsoft', 'Razer'])).astype(int)

feature_cols = [
    'Brand_Encoded', 'Processor_Encoded', 'Generation_Encoded', 'RAM_GB',
    'Storage_Type_Encoded', 'Storage_GB', 'Screen_Size', 'GPU_Encoded',
    'OS_Encoded', 'Weight_kg', 'Touchscreen', 'Warranty_Years',
    'Storage_RAM_Ratio', 'Is_Gaming', 'Is_Premium'
]

X = df[feature_cols]
y = df['Price_INR']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining Random Forest...")
model = RandomForestRegressor(
    n_estimators=300, max_depth=20,
    min_samples_split=2, min_samples_leaf=1,
    random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
test_r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print(f"  Test R²  : {test_r2:.4f}")
print(f"  RMSE     : Rs.{rmse:,.0f}")
print(f"  MAE      : Rs.{mae:,.0f}")

# Feature importance
fi = pd.DataFrame({'Feature': feature_cols, 'Importance': model.feature_importances_})
print("\nTop Features:")
print(fi.sort_values('Importance', ascending=False).head(8).to_string(index=False))

# Save artifacts
joblib.dump(model, 'models/laptop_price_model.pkl')
joblib.dump(label_encoders, 'models/label_encoders.pkl')
joblib.dump(feature_cols, 'models/feature_columns.pkl')
joblib.dump({
    'model_name': 'Random Forest',
    'test_r2': test_r2,
    'rmse': rmse,
    'mae': mae,
    'currency': 'INR',
    'features': feature_cols
}, 'models/model_metadata.pkl')

print("\nModel saved successfully!")
print("="*60)
