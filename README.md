# 🖥️ Laptop Price Prediction System - SmartTech Co.

## 📋 Project Overview

A complete end-to-end machine learning project that predicts laptop prices based on specifications. This project includes data generation, model training, evaluation, and a real-time web application for predictions.

## 🎯 Business Objectives

- **Accurate Pricing**: Predict laptop prices with high accuracy (R² > 0.95)
- **Market Positioning**: Understand feature impact on pricing
- **Brand Influence**: Assess brand reputation effects on pricing
- **Real-time Predictions**: Web application for instant price estimates

## 🚀 Features

- ✅ Synthetic dataset generation with realistic laptop specifications
- ✅ Comprehensive data exploration and analysis
- ✅ Multiple ML algorithms comparison (Linear, Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost)
- ✅ Feature engineering for improved predictions
- ✅ Real-time web application with Flask
- ✅ Professional UI with responsive design
- ✅ Model performance metrics and visualization

## 📁 Project Structure

```
laptop_price_prediction/
├── data/
│   └── laptop_data.csv          # Generated dataset
├── models/
│   ├── laptop_price_model.pkl   # Trained model
│   ├── label_encoders.pkl       # Categorical encoders
│   ├── feature_columns.pkl      # Feature list
│   └── model_metadata.pkl       # Model info
├── notebooks/
│   └── 01_data_exploration.py   # EDA script
├── static/
│   └── css/
│       └── style.css            # Web UI styles
├── templates/
│   └── index.html               # Web interface
├── generate_data.py             # Dataset generator
├── train_model.py               # Model training
├── app.py                       # Flask web app
└── requirements.txt             # Dependencies
```

## 🛠️ Installation & Setup

### Step 1: Install Dependencies

```bash
cd laptop_price_prediction
pip install -r requirements.txt
```

### Step 2: Generate Dataset

```bash
python generate_data.py
```

This creates a dataset with 1000 laptop samples with realistic specifications and prices.

### Step 3: Explore Data (Optional)

```bash
python notebooks/01_data_exploration.py
```

### Step 4: Train Model

```bash
python train_model.py
```

This will:
- Load and preprocess data
- Engineer features
- Train 6 different models
- Compare performance
- Save the best model

### Step 5: Run Web Application

```bash
python app.py
```

Access the application at: **http://127.0.0.1:5000**

## 📊 Model Performance

The system trains and compares multiple models:

| Model | Expected R² Score | RMSE |
|-------|------------------|------|
| XGBoost | ~0.98 | ~$50 |
| Random Forest | ~0.97 | ~$60 |
| Gradient Boosting | ~0.96 | ~$70 |
| Ridge Regression | ~0.92 | ~$100 |
| Linear Regression | ~0.91 | ~$110 |
| Lasso Regression | ~0.90 | ~$120 |

## 🎨 Web Application Features

### User Interface
- Modern, responsive design
- Gradient backgrounds
- Easy-to-use form inputs
- Real-time predictions
- Price range estimates
- Specifications summary

### Input Features
1. **Brand**: Dell, HP, Lenovo, Apple, Asus, Acer, MSI, Microsoft, Razer, Samsung
2. **Processor**: Intel Core i3/i5/i7/i9, AMD Ryzen 3/5/7/9, Apple M1/M2
3. **RAM**: 4GB, 8GB, 16GB, 32GB, 64GB
4. **Storage Type**: HDD, SSD, Hybrid
5. **Storage Size**: 256GB, 512GB, 1TB, 2TB
6. **Screen Size**: 13.3", 14.0", 15.6", 17.3"
7. **GPU**: Integrated, NVIDIA GTX/RTX series, AMD Radeon
8. **Operating System**: Windows 10/11, macOS, Linux
9. **Weight**: 1.2kg - 2.5kg
10. **Touchscreen**: Yes/No
11. **Warranty**: 1-3 years

## 🔍 Key Insights

### Most Important Features for Pricing:
1. **Processor** - High-end processors significantly increase price
2. **Brand** - Premium brands (Apple, Microsoft, Razer) command higher prices
3. **GPU** - Dedicated graphics cards add substantial value
4. **RAM** - More RAM correlates with higher prices
5. **Storage Type & Size** - SSDs and larger storage increase price

### Brand Analysis:
- **Premium Tier**: Apple, Microsoft, Razer ($1500-$3000)
- **Mid-Range**: Dell, HP, Asus, MSI ($800-$1500)
- **Budget**: Acer, Lenovo ($500-$1000)

## 📈 Feature Engineering

The model uses engineered features:
- `Storage_RAM_Ratio`: Storage to RAM ratio
- `Is_Gaming`: Gaming laptop indicator (GPU + RAM >= 16GB)
- `Is_Premium`: Premium brand indicator
- Encoded categorical variables

## 🎯 Model Capabilities

### Strengths:
✅ High accuracy on diverse specifications
✅ Handles both budget and high-end laptops
✅ Accounts for brand premium
✅ Real-time predictions
✅ Interpretable results

### Limitations:
⚠️ Based on synthetic data (replace with real market data)
⚠️ Doesn't account for market trends over time
⚠️ Limited to predefined brands and specifications
⚠️ Doesn't consider seasonal pricing variations

## 🔄 Real-time Prediction Workflow

1. User enters laptop specifications
2. Web form validates inputs
3. Data sent to Flask backend
4. Features encoded and engineered
5. Model makes prediction
6. Price displayed with confidence range
7. Specifications summary shown

## 📱 API Endpoints

### `GET /`
Returns the main web interface

### `POST /predict`
Accepts JSON with laptop specifications, returns predicted price

**Request Body:**
```json
{
  "brand": "Dell",
  "processor": "Intel Core i7",
  "ram": "16",
  "storage_type": "SSD",
  "storage": "512",
  "screen_size": "15.6",
  "gpu": "NVIDIA RTX 3060",
  "os": "Windows 11",
  "weight": "2.0",
  "touchscreen": "1",
  "warranty": "2"
}
```

**Response:**
```json
{
  "success": true,
  "predicted_price": 1250.50,
  "price_range": {
    "min": 1187.98,
    "max": 1312.03
  },
  "specifications": {...}
}
```

### `GET /model-info`
Returns model metadata and performance metrics

## 🚀 Deployment Options

### Local Deployment
```bash
python app.py
```

### Production Deployment (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t laptop-price-predictor .
docker run -p 5000:5000 laptop-price-predictor
```

## 📊 Future Enhancements

1. **Real Market Data**: Replace synthetic data with actual market prices
2. **Time Series**: Add temporal features for price trends
3. **More Features**: Battery life, build quality, customer reviews
4. **Advanced Models**: Deep learning, ensemble methods
5. **A/B Testing**: Compare model versions
6. **User Feedback**: Collect actual vs predicted prices
7. **Mobile App**: Native mobile application
8. **API Authentication**: Secure API endpoints

## 🤝 Contributing

This is a demonstration project for SmartTech Co. For production use:
1. Replace synthetic data with real market data
2. Retrain models regularly with new data
3. Add monitoring and logging
4. Implement CI/CD pipeline
5. Add unit and integration tests

## 📄 License

This project is created for educational and demonstration purposes.

## 👥 Team

Data Science Team - SmartTech Co.

## 📞 Support

For questions or issues, please contact the data science team.

---

**Note**: This project uses synthetic data for demonstration. For production deployment, use real market data and implement proper data collection, validation, and monitoring systems.
