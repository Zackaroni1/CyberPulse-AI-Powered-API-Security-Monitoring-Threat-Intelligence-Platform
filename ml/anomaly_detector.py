import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_PATH = "ml/isolation_forest_model.pkl"
SCALER_PATH = "ml/scaler.pkl"

FEATURES = [
    "response_time_ms",
    "request_count_last_minute",
    "failed_attempts",
    "status_code",
]

def extract_features(logs: list) -> pd.DataFrame:
    """Convert raw logs into ML feature matrix"""
    rows = []
    for log in logs:
        rows.append({
            "response_time_ms": log.get("response_time_ms", 0),
            "request_count_last_minute": log.get("request_count_last_minute", 0),
            "failed_attempts": log.get("failed_attempts", 0),
            "status_code": log.get("status_code", 200),
        })
    return pd.DataFrame(rows)

def train_model(logs: list):
    """Train Isolation Forest on log data"""
    df = extract_features(logs)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,  # expect 20% anomalies
        random_state=42
    )
    model.fit(X_scaled)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    return model, scaler

def predict_anomalies(logs: list):
    """Predict which logs are anomalies"""
    if not os.path.exists(MODEL_PATH):
        return None

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    df = extract_features(logs)
    X_scaled = scaler.transform(df)
    predictions = model.predict(X_scaled)  # 1 = normal, -1 = anomaly
    scores = model.decision_function(X_scaled)

    results = []
    for i, log in enumerate(logs):
        log_copy = log.copy()
        log_copy["ml_is_anomaly"] = bool(predictions[i] == -1)
        log_copy["anomaly_score"] = round(float(scores[i]), 4)
        results.append(log_copy)

    return results