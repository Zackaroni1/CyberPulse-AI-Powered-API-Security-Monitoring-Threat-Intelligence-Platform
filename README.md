# ThreatWatch — Real-Time Log Intelligence & Threat Classification

A real-time security monitoring system that analyzes API logs using Machine Learning to detect anomalies and classify cyber threats automatically.

## What it does
- Monitors API traffic in real-time
- Detects anomalies using Isolation Forest ML algorithm
- Classifies threats: Brute Force, Bot Traffic, Rate Limit Violation, Suspicious IP, DDoS
- Displays live alerts on a professional dashboard

## Tech Stack
- **Backend:** Python, FastAPI
- **Machine Learning:** scikit-learn (Isolation Forest)
- **Dashboard:** Streamlit, Plotly
- **Data Processing:** Pandas, NumPy

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/VISHAL-RAJA-25/log-intelligence-system.git
cd log-intelligence-system
```

### 2. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the backend
```bash
uvicorn backend.main:app --reload
```

### 4. Start the dashboard
```bash
streamlit run dashboard/app.py
```

### 5. Use the dashboard
- Click **Generate Logs** to simulate traffic
- Click **Train Model** to train the ML model
- Click **Analyze Threats** to detect and classify attacks

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /generate-logs | Generate simulated traffic logs |
| POST | /train | Train the Isolation Forest model |
| POST | /analyze | Run ML anomaly detection |
| GET | /logs | Fetch recent logs |
| GET | /stats | Get traffic statistics |
| DELETE | /logs | Clear all logs |

## Threat Types Detected
| Threat | Description |
|--------|-------------|
| Brute Force | Repeated failed login attempts |
| Bot Traffic | Abnormally high request frequency |
| Rate Limit Violation | Exceeding API request limits |
| Suspicious IP | Unauthorized access to admin endpoints |
| DDoS Attempt | Server flooding with high response times |
