import pickle
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "soil_model.pkl")

class SoilHealthModel:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Soil model file not found. Please run train_model.py first.")
        with open(MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)

    def predict_health(self, ndvi, moisture=None, ph=None):
        features = [ndvi]
        if moisture is not None:
            features.append(moisture)
        if ph is not None:
            features.append(ph)
        else:
            while len(features) < self.model.n_features_in_:
                features.append(0.5)
        X = np.array([features])
        pred = self.model.predict(X)[0]
        proba = self.model.predict_proba(X)[0].max()
        return pred, float(proba)
