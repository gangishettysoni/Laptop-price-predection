@echo off
echo ============================================================
echo LAPTOP PRICE PREDICTION - SMARTTECH CO.
echo Automated Setup and Execution Script
echo ============================================================
echo.

echo Step 1: Installing Dependencies...
echo ------------------------------------------------------------
py -m pip install -q pandas numpy scikit-learn matplotlib seaborn flask joblib xgboost
echo Dependencies installed successfully!
echo.

echo Step 2: Generating Dataset...
echo ------------------------------------------------------------
py generate_data.py
echo.

echo Step 3: Training Models...
echo ------------------------------------------------------------
py train_model.py
echo.

echo Step 4: Starting Web Application...
echo ------------------------------------------------------------
echo.
echo ============================================================
echo WEB APPLICATION READY!
echo Access at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.
py app.py
