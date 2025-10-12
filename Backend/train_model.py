"""
Train a model for soil health classification. For competition we produce:
 - synthetic (but realistic) dataset using NDVI and some noise
 - RandomForest classifier and SHAP explainability
Produces:
 - backend/soil_model.pkl
 - backend/reports/shap_summary.png
"""
print("✅ train_model.py is running...")

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import shap
import matplotlib.pyplot as plt
import random

random.seed(42)
np.random.seed(42)

OUT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "soil_model.pkl")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_dataset(n=5000):
    # create NDVI values and synthetic features (NDVI + noise)
    ndvi = np.random.uniform(-0.05, 0.85, size=n)
    # add a dummy moisture-like signal derived from ndvi + noise
    moisture = ndvi * 0.6 + np.random.normal(0, 0.05, size=n)
    temp_index = 1 - (ndvi * 0.3) + np.random.normal(0, 0.03, size=n)
    # labels based on NDVI thresholds with slight randomness
    labels = []
    for x in ndvi:
        if x < 0.25:
            labels.append("Highly Degraded")
        elif x < 0.5:
            labels.append("Moderately Degraded")
        else:
            labels.append("Healthy")
    df = pd.DataFrame({"ndvi": ndvi, "moisture": moisture, "temp_idx": temp_index, "label": labels})
    return df

def train_and_save():
    df = generate_dataset()
    X = df[["ndvi", "moisture", "temp_idx"]].values
    y = df["label"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=250, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    # Save model
    joblib.dump(clf, OUT_MODEL_PATH)
    print("Model saved to", OUT_MODEL_PATH)

    # SHAP explainability
    try:
        explainer = shap.TreeExplainer(clf)
        shap_values = explainer.shap_values(X_test)
        # summary plot, class 0..n; show aggregated importance
        plt.figure(figsize=(6,4))
        shap.summary_plot(shap_values, X_test, show=False, feature_names=["ndvi","moisture","temp_idx"])
        plt.title("SHAP summary (multi-class)")
        plt.tight_layout()
        out = os.path.join(REPORTS_DIR, "shap_summary.png")
        plt.savefig(out, dpi=150)
        plt.close()
        print("SHAP summary saved to", out)
    except Exception as e:
        print("SHAP generation failed:", e)

if __name__ == "__main__":
    train_and_save()
