from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

model = joblib.load('models/laptop_price_model.pkl')
label_encoders = joblib.load('models/label_encoders.pkl')
feature_cols = joblib.load('models/feature_columns.pkl')
metadata = joblib.load('models/model_metadata.pkl')

INR_TO_USD = 0.012  # 1 INR = 0.012 USD (approx ₹83.5 = $1)

brands = ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus', 'Acer', 'MSI', 'Microsoft', 'Razer', 'Samsung']
processors = ['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core i9',
              'AMD Ryzen 3', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9', 'Apple M1', 'Apple M2']

processor_generations = {
    'Intel Core i3': ['10th Gen', '11th Gen', '12th Gen', '13th Gen'],
    'Intel Core i5': ['10th Gen', '11th Gen', '12th Gen', '13th Gen', '14th Gen'],
    'Intel Core i7': ['11th Gen', '12th Gen', '13th Gen', '14th Gen'],
    'Intel Core i9': ['12th Gen', '13th Gen', '14th Gen'],
    'AMD Ryzen 3': ['Ryzen 5000', 'Ryzen 6000', 'Ryzen 7000'],
    'AMD Ryzen 5': ['Ryzen 5000', 'Ryzen 6000', 'Ryzen 7000'],
    'AMD Ryzen 7': ['Ryzen 5000', 'Ryzen 6000', 'Ryzen 7000'],
    'AMD Ryzen 9': ['Ryzen 6000', 'Ryzen 7000'],
    'Apple M1': ['M1', 'M1 Pro', 'M1 Max'],
    'Apple M2': ['M2', 'M2 Pro', 'M2 Max'],
}

storage_types = ['HDD', 'SSD', 'Hybrid']
gpus = ['Integrated', 'NVIDIA GTX 1650', 'NVIDIA RTX 3050', 'NVIDIA RTX 3060',
        'NVIDIA RTX 3070', 'NVIDIA RTX 4060', 'AMD Radeon']
os_types = ['Windows 10', 'Windows 11', 'macOS', 'Linux']

@app.route('/')
def home():
    return render_template('index.html',
                           brands=brands,
                           processors=processors,
                           processor_generations=processor_generations,
                           storage_types=storage_types,
                           gpus=gpus,
                           os_types=os_types,
                           model_info=metadata)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        brand_enc = label_encoders['Brand'].transform([data['brand']])[0]
        processor_enc = label_encoders['Processor'].transform([data['processor']])[0]
        generation_enc = label_encoders['Generation'].transform([data['generation']])[0]
        storage_type_enc = label_encoders['Storage_Type'].transform([data['storage_type']])[0]
        gpu_enc = label_encoders['GPU'].transform([data['gpu']])[0]
        os_enc = label_encoders['OS'].transform([data['os']])[0]

        ram_gb = int(data['ram'])
        storage_gb = int(data['storage'])
        screen_size = float(data['screen_size'])
        weight_kg = float(data['weight'])
        touchscreen = int(data['touchscreen'])
        warranty_years = int(data['warranty'])

        storage_ram_ratio = storage_gb / ram_gb
        is_gaming = 1 if (data['gpu'] != 'Integrated' and ram_gb >= 16) else 0
        is_premium = 1 if data['brand'] in ['Apple', 'Microsoft', 'Razer'] else 0

        # Build DataFrame with exact column names the model was trained on
        input_df = pd.DataFrame([{
            'Brand_Encoded': brand_enc,
            'Processor_Encoded': processor_enc,
            'Generation_Encoded': generation_enc,
            'RAM_GB': ram_gb,
            'Storage_Type_Encoded': storage_type_enc,
            'Storage_GB': storage_gb,
            'Screen_Size': screen_size,
            'GPU_Encoded': gpu_enc,
            'OS_Encoded': os_enc,
            'Weight_kg': weight_kg,
            'Touchscreen': touchscreen,
            'Warranty_Years': warranty_years,
            'Storage_RAM_Ratio': storage_ram_ratio,
            'Is_Gaming': is_gaming,
            'Is_Premium': is_premium
        }])

        price_inr = model.predict(input_df)[0]
        price_usd = price_inr * INR_TO_USD

        return jsonify({
            'success': True,
            'price_inr': round(price_inr, -2),
            'price_usd': round(price_usd, 2),
            'range_inr': {'min': round(price_inr * 0.95, -2), 'max': round(price_inr * 1.05, -2)},
            'range_usd': {'min': round(price_usd * 0.95, 2), 'max': round(price_usd * 1.05, 2)},
            'specifications': {
                'Brand': data['brand'],
                'Processor': f"{data['processor']} ({data['generation']})",
                'RAM': f"{ram_gb} GB",
                'Storage': f"{storage_gb} GB {data['storage_type']}",
                'Screen': f"{screen_size}\"",
                'GPU': data['gpu'],
                'OS': data['os']
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generations/<processor>')
def get_generations(processor):
    return jsonify(processor_generations.get(processor, []))

@app.route('/model-info')
def model_info():
    return jsonify(metadata)

if __name__ == '__main__':
    print("="*60)
    print("LAPTOP PRICE PREDICTION - WEB APPLICATION")
    print(f"Model : {metadata['model_name']}")
    print(f"R²    : {metadata['test_r2']:.4f}")
    print(f"RMSE  : Rs.{metadata['rmse']:,.0f}")
    print("Access: http://127.0.0.1:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
