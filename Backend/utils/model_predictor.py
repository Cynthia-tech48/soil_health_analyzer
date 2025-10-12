"""
Predict soil health from NDVI using trained model or fallback heuristic.
"""

import os
import joblib
import numpy as np

# Path to trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "soil_model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

# Load model once at import
_model = None
if os.path.exists(MODEL_PATH):
    try:
        _model = joblib.load(MODEL_PATH)
        print("Loaded model:", MODEL_PATH)
    except Exception as e:
        print("Failed to load model:", e)
        _model = None
else:
    print("Model file not found at", MODEL_PATH)


def predict_soil_health_from_ndvi(ndvi_value):
    """
    Predict soil health from a single NDVI value.
    
    Input:
        ndvi_value (float): NDVI value, e.g., 0.4
    
    Output:
        label (str): "Healthy", "Moderately Degraded", or "Highly Degraded"
        score (float): 0-100 health score
    """
    try:
        x = float(ndvi_value)
    except Exception:
        x = 0.0

    # Score mapping NDVI -> 0-100
    score = max(0.0, min(100.0, (x + 0.2) * 100 / 1.1))

    if _model:
        # Model expects array of shape (n_samples, n_features)
        # For training, features were [ndvi, moisture, temp_idx]
        moisture = x * 0.6  # dummy
        temp_idx = 1 - (x * 0.3)
        X = np.array([[x, moisture, temp_idx]])
        try:
            pred = _model.predict(X)
            label = str(pred[0])
        except Exception as e:
            print("Model prediction failed:", e)
            label = "Unknown"
    else:
        # Heuristic fallback
        if x < 0.25:
            label = "Highly Degraded"
        elif x < 0.5:
            label = "Moderately Degraded"
        else:
            label = "Healthy"

    return label, round(float(score), 2)
