import joblib
import numpy as np

print("="*60)
print("LAPTOP PRICE PREDICTION - TEST SCRIPT")
print("="*60)

# Load model and artifacts
print("\nLoading model and artifacts...")
model = joblib.load('models/laptop_price_model.pkl')
label_encoders = joblib.load('models/label_encoders.pkl')
metadata = joblib.load('models/model_metadata.pkl')

print(f"Model: {metadata['model_name']}")
print(f"Test R²: {metadata['test_r2']:.4f}")
print(f"RMSE: ${metadata['rmse']:.2f}")
print(f"MAE: ${metadata['mae']:.2f}")

# Test cases
test_cases = [
    {
        'name': 'Budget Laptop',
        'brand': 'Acer',
        'processor': 'Intel Core i3',
        'ram': 8,
        'storage_type': 'HDD',
        'storage': 512,
        'screen_size': 15.6,
        'gpu': 'Integrated',
        'os': 'Windows 10',
        'weight': 2.0,
        'touchscreen': 0,
        'warranty': 1
    },
    {
        'name': 'Mid-Range Laptop',
        'brand': 'Dell',
        'processor': 'Intel Core i5',
        'ram': 16,
        'storage_type': 'SSD',
        'storage': 512,
        'screen_size': 15.6,
        'gpu': 'NVIDIA GTX 1650',
        'os': 'Windows 11',
        'weight': 1.8,
        'touchscreen': 0,
        'warranty': 2
    },
    {
        'name': 'Gaming Laptop',
        'brand': 'MSI',
        'processor': 'Intel Core i7',
        'ram': 32,
        'storage_type': 'SSD',
        'storage': 1024,
        'screen_size': 17.3,
        'gpu': 'NVIDIA RTX 3070',
        'os': 'Windows 11',
        'weight': 2.5,
        'touchscreen': 0,
        'warranty': 2
    },
    {
        'name': 'Premium MacBook',
        'brand': 'Apple',
        'processor': 'Apple M2',
        'ram': 16,
        'storage_type': 'SSD',
        'storage': 512,
        'screen_size': 13.3,
        'gpu': 'Integrated',
        'os': 'macOS',
        'weight': 1.2,
        'touchscreen': 0,
        'warranty': 1
    }
]

print("\n" + "="*60)
print("TEST PREDICTIONS")
print("="*60)

for test in test_cases:
    # Encode features
    brand_encoded = label_encoders['Brand'].transform([test['brand']])[0]
    processor_encoded = label_encoders['Processor'].transform([test['processor']])[0]
    storage_type_encoded = label_encoders['Storage_Type'].transform([test['storage_type']])[0]
    gpu_encoded = label_encoders['GPU'].transform([test['gpu']])[0]
    os_encoded = label_encoders['OS'].transform([test['os']])[0]
    
    # Calculate engineered features
    storage_ram_ratio = test['storage'] / test['ram']
    is_gaming = 1 if (test['gpu'] != 'Integrated' and test['ram'] >= 16) else 0
    is_premium = 1 if test['brand'] in ['Apple', 'Microsoft', 'Razer'] else 0
    
    # Create feature array
    features = np.array([[
        brand_encoded, processor_encoded, test['ram'], storage_type_encoded,
        test['storage'], test['screen_size'], gpu_encoded, os_encoded, test['weight'],
        test['touchscreen'], test['warranty'], storage_ram_ratio, is_gaming, is_premium
    ]])
    
    # Predict
    predicted_price = model.predict(features)[0]
    
    print(f"\n{test['name']}:")
    print(f"  Brand: {test['brand']}")
    print(f"  Processor: {test['processor']}")
    print(f"  RAM: {test['ram']} GB")
    print(f"  Storage: {test['storage']} GB {test['storage_type']}")
    print(f"  GPU: {test['gpu']}")
    print(f"  Predicted Price: ${predicted_price:.2f}")

print("\n" + "="*60)
print("TEST COMPLETED SUCCESSFULLY")
print("="*60)
