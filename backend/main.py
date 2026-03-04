from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.log_generator import generate_log_batch
from ml.anomaly_detector import train_model, predict_anomalies
from ml.threat_classifier import classify_threat

app = FastAPI(title="Log Intelligence System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

log_store = []

@app.get("/")
def root():
    return {"message": "Log Intelligence System Running"}

@app.post("/generate-logs")
def generate_logs(total: int = 20, attack_ratio: float = 0.2):
    logs = generate_log_batch(total=total, attack_ratio=attack_ratio)
    log_store.extend(logs)
    return {
        "message": f"Generated {total} logs",
        "total_in_store": len(log_store)
    }

@app.post("/train")
def train():
    """Train the ML model on current logs"""
    if len(log_store) < 10:
        return {"error": "Need at least 10 logs. Call /generate-logs first."}

    train_model(log_store)
    return {
        "message": "Model trained successfully",
        "trained_on": len(log_store)
    }

@app.post("/analyze")
def analyze():
    """Run ML anomaly detection + threat classification on all logs"""
    if len(log_store) < 10:
        return {"error": "Need at least 10 logs first."}

    results = predict_anomalies(log_store)
    if results is None:
        return {"error": "Model not trained yet. Call /train first."}

    for log in results:
        log["threat_type"] = classify_threat(log)

    anomalies = [l for l in results if l["ml_is_anomaly"]]

    threat_counts = {}
    for log in anomalies:
        t = log["threat_type"]
        threat_counts[t] = threat_counts.get(t, 0) + 1

    return {
        "total_logs": len(results),
        "anomalies_detected": len(anomalies),
        "anomaly_rate": f"{round(len(anomalies)/len(results)*100, 1)}%",
        "threat_breakdown": threat_counts,
        "anomalies": anomalies[:5]
    }

@app.get("/logs")
def get_logs(limit: int = 50):
    return {"total": len(log_store), "logs": log_store[-limit:]}

@app.get("/stats")
def get_stats():
    if not log_store:
        return {"message": "No logs yet."}
    total = len(log_store)
    anomalies = [l for l in log_store if l.get("is_anomaly")]
    threat_types = {}
    for log in anomalies:
        t = log.get("threat_type", "unknown")
        threat_types[t] = threat_types.get(t, 0) + 1
    return {
        "total_requests": total,
        "total_anomalies": len(anomalies),
        "anomaly_percentage": round(len(anomalies) / total * 100, 2),
        "threat_breakdown": threat_types
    }

@app.delete("/logs")
def clear_logs():
    log_store.clear()
    return {"message": "Logs cleared"}