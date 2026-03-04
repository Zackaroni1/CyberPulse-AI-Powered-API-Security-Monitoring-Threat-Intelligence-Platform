import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ThreatWatch — Log Intelligence",
    page_icon="assets/favicon.ico" if False else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Professional CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

* { font-family: 'IBM Plex Sans', sans-serif; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0e1a;
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background-color: #0d1117;
    border-right: 1px solid #1e2d3d;
}

[data-testid="stSidebar"] * { color: #94a3b8 !important; }

.sidebar-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3b82f6 !important;
    padding: 16px 0 8px 0;
    border-bottom: 1px solid #1e2d3d;
    margin-bottom: 16px;
}

.stButton > button {
    background: transparent;
    border: 1px solid #1e2d3d;
    color: #94a3b8 !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
    padding: 10px 16px;
    width: 100%;
    text-align: left;
    transition: all 0.2s ease;
    border-radius: 4px;
    margin-bottom: 6px;
}

.stButton > button:hover {
    background: #1e2d3d;
    border-color: #3b82f6;
    color: #3b82f6 !important;
}

.header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 24px 0;
    border-bottom: 1px solid #1e2d3d;
    margin-bottom: 32px;
}

.header-title {
    font-size: 22px;
    font-weight: 600;
    color: #f1f5f9;
    letter-spacing: -0.5px;
}

.header-sub {
    font-size: 12px;
    color: #475569;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 8px #22c55e;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.metric-card {
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-radius: 8px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, transparent);
}

.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace;
}

.metric-value {
    font-size: 32px;
    font-weight: 600;
    color: #f1f5f9;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}

.metric-value.danger { color: #ef4444; }
.metric-value.warning { color: #f59e0b; }
.metric-value.success { color: #22c55e; }
.metric-value.info { color: #3b82f6; }

.metric-sub {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
    font-family: 'IBM Plex Mono', monospace;
}

.section-header {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d3d;
}

.alert-card {
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-left: 3px solid #ef4444;
    border-radius: 4px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
}

.alert-card.brute_force { border-left-color: #ef4444; }
.alert-card.bot_traffic { border-left-color: #f59e0b; }
.alert-card.rate_limit_violation { border-left-color: #8b5cf6; }
.alert-card.suspicious_ip { border-left-color: #ec4899; }
.alert-card.ddos_attempt { border-left-color: #06b6d4; }
.alert-card.unknown_anomaly { border-left-color: #6b7280; }

.alert-threat {
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.alert-threat.brute_force { color: #ef4444; }
.alert-threat.bot_traffic { color: #f59e0b; }
.alert-threat.rate_limit_violation { color: #8b5cf6; }
.alert-threat.suspicious_ip { color: #ec4899; }
.alert-threat.ddos_attempt { color: #06b6d4; }
.alert-threat.unknown_anomaly { color: #6b7280; }

.alert-meta { color: #475569; font-size: 11px; }
.alert-ip { color: #94a3b8; }

.no-threat {
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-left: 3px solid #22c55e;
    border-radius: 4px;
    padding: 14px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #22c55e;
    letter-spacing: 1px;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

.stDataFrame { border: 1px solid #1e2d3d; border-radius: 8px; overflow: hidden; }

div[data-testid="metric-container"] { display: none; }

.stSlider > div > div > div { background: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">ThreatWatch v1.0</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Configuration</div>', unsafe_allow_html=True)

    total_logs = st.slider("Log Volume", 20, 200, 50, help="Number of requests to simulate")
    attack_ratio = st.slider("Attack Ratio", 0.05, 0.60, 0.20, help="Fraction of malicious traffic")

    st.markdown('<div class="sidebar-title">Actions</div>', unsafe_allow_html=True)

    if st.button("GENERATE LOGS"):
        with st.spinner("Generating traffic..."):
            res = requests.post(f"{API_URL}/generate-logs?total={total_logs}&attack_ratio={attack_ratio}")
            if res.status_code == 200:
                st.success(f"Generated {total_logs} log entries")
            else:
                st.error("Generation failed")

    if st.button("TRAIN MODEL"):
        with st.spinner("Training Isolation Forest..."):
            res = requests.post(f"{API_URL}/train")
            if res.status_code == 200:
                st.success("Model trained successfully")
            else:
                st.error("Training failed")

    if st.button("ANALYZE THREATS"):
        with st.spinner("Running ML analysis..."):
            res = requests.post(f"{API_URL}/analyze")
            if res.status_code == 200:
                st.success("Analysis complete")
            else:
                st.error("Analysis failed")

    if st.button("CLEAR ALL LOGS"):
        requests.delete(f"{API_URL}/logs")
        st.warning("Log store cleared")

    st.markdown('<div class="sidebar-title">System</div>', unsafe_allow_html=True)
    auto_refresh = st.checkbox("Live Refresh (5s)", value=False)

# ── Header ──
st.markdown("""
<div class="header-bar">
    <div>
        <div class="header-title">Log Intelligence & Threat Classification</div>
        <div class="header-sub">Real-time anomaly detection powered by Isolation Forest ML</div>
    </div>
    <div style="text-align:right">
        <div style="font-size:12px; color:#475569; font-family:'IBM Plex Mono',monospace;">
            <span class="status-dot"></span>SYSTEM ONLINE
        </div>
        <div style="font-size:11px; color:#1e2d3d; margin-top:4px; font-family:'IBM Plex Mono',monospace;">
            FastAPI + Isolation Forest
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Fetch Data ──
try:
    stats_res = requests.get(f"{API_URL}/stats", timeout=3)
    logs_res = requests.get(f"{API_URL}/logs?limit=200", timeout=3)
    analyze_res = requests.post(f"{API_URL}/analyze", timeout=5)

    stats = stats_res.json()
    logs_data = logs_res.json()
    analyze_data = analyze_res.json()
    logs = logs_data.get("logs", [])

    total = stats.get("total_requests", 0)
    anomalies = stats.get("total_anomalies", 0)
    anomaly_pct = stats.get("anomaly_percentage", 0)
    threat_types = stats.get("threat_breakdown", {})
    safe = total - anomalies

    # ── Metric Cards ──
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Requests</div>
            <div class="metric-value info">{total:,}</div>
            <div class="metric-sub">logged events</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Threats Detected</div>
            <div class="metric-value danger">{anomalies:,}</div>
            <div class="metric-sub">anomalous requests</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        color = "danger" if anomaly_pct > 30 else "warning" if anomaly_pct > 10 else "success"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Anomaly Rate</div>
            <div class="metric-value {color}">{anomaly_pct}%</div>
            <div class="metric-sub">of total traffic</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Clean Traffic</div>
            <div class="metric-value success">{safe:,}</div>
            <div class="metric-sub">safe requests</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    chart_col1, chart_col2 = st.columns(2)

    CHART_COLORS = ["#3b82f6", "#ef4444", "#f59e0b", "#22c55e", "#8b5cf6", "#ec4899"]

    with chart_col1:
        st.markdown('<div class="section-header">Threat Distribution</div>', unsafe_allow_html=True)
        if threat_types:
            fig = go.Figure(data=[go.Pie(
                labels=list(threat_types.keys()),
                values=list(threat_types.values()),
                hole=0.65,
                marker=dict(colors=CHART_COLORS, line=dict(color='#0a0e1a', width=2)),
                textfont=dict(family="IBM Plex Mono", size=11, color="#94a3b8"),
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>"
            )])
            fig.add_annotation(
                text=f"<b>{sum(threat_types.values())}</b><br><span style='font-size:10px'>threats</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, color="#f1f5f9", family="IBM Plex Mono")
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#94a3b8", family="IBM Plex Mono"),
                showlegend=True,
                legend=dict(
                    font=dict(size=11, family="IBM Plex Mono", color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)",
                    x=1, y=0.5
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                height=280
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div class="no-threat">No threat data. Run analysis first.</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="section-header">Status Code Distribution</div>', unsafe_allow_html=True)
        if logs:
            df = pd.DataFrame(logs)
            status_counts = df["status_code"].value_counts().reset_index()
            status_counts.columns = ["status_code", "count"]
            status_counts["status_code"] = status_counts["status_code"].astype(str)

            status_color_map = {
                "200": "#22c55e", "201": "#22c55e", "204": "#22c55e",
                "401": "#ef4444", "403": "#ef4444", "404": "#f59e0b",
                "429": "#8b5cf6", "500": "#ef4444"
            }
            colors = [status_color_map.get(s, "#3b82f6") for s in status_counts["status_code"]]

            fig2 = go.Figure(data=[go.Bar(
                x=status_counts["status_code"],
                y=status_counts["count"],
                marker=dict(color=colors, line=dict(color='#0a0e1a', width=1)),
                hovertemplate="<b>HTTP %{x}</b><br>Count: %{y}<extra></extra>"
            )])
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#94a3b8", family="IBM Plex Mono", size=11),
                xaxis=dict(showgrid=False, color="#475569"),
                yaxis=dict(showgrid=True, gridcolor="#1e2d3d", color="#475569"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Response Time Chart ──
    st.markdown('<div class="section-header">Response Latency by Endpoint (ms)</div>', unsafe_allow_html=True)
    if logs:
        df = pd.DataFrame(logs)
        fig3 = go.Figure()
        for i, endpoint in enumerate(df["endpoint"].unique()):
            ep_data = df[df["endpoint"] == endpoint]["response_time_ms"]
            fig3.add_trace(go.Box(
                y=ep_data,
                name=endpoint,
                marker_color=CHART_COLORS[i % len(CHART_COLORS)],
                line=dict(color=CHART_COLORS[i % len(CHART_COLORS)]),
                fillcolor=f"rgba({int(CHART_COLORS[i % len(CHART_COLORS)][1:3], 16)},{int(CHART_COLORS[i % len(CHART_COLORS)][3:5], 16)},{int(CHART_COLORS[i % len(CHART_COLORS)][5:7], 16)},0.1)"
            ))
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94a3b8", family="IBM Plex Mono", size=11),
            xaxis=dict(showgrid=False, color="#475569"),
            yaxis=dict(showgrid=True, gridcolor="#1e2d3d", color="#475569", title="ms"),
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10))
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live Alerts ──
    st.markdown('<div class="section-header">Live Threat Alerts</div>', unsafe_allow_html=True)
    anomaly_logs = [l for l in logs if l.get("is_anomaly")]

    if anomaly_logs:
        for log in reversed(anomaly_logs[-12:]):
            threat = log.get("threat_type", "unknown_anomaly")
            ip = log.get("ip_address", "—")
            endpoint = log.get("endpoint", "—")
            status = log.get("status_code", "—")
            ts = log.get("timestamp", "")[:19].replace("T", " ")
            reqs = log.get("request_count_last_minute", 0)
            fails = log.get("failed_attempts", 0)

            st.markdown(f"""
            <div class="alert-card {threat}">
                <div>
                    <span class="alert-threat {threat}">{threat.replace('_', ' ').upper()}</span>
                    <span class="alert-meta"> &nbsp;|&nbsp; </span>
                    <span class="alert-ip">{ip}</span>
                    <span class="alert-meta"> &nbsp;→&nbsp; {endpoint} &nbsp;|&nbsp; HTTP {status}</span>
                </div>
                <div class="alert-meta">{reqs} req/min &nbsp;|&nbsp; {fails} failures &nbsp;|&nbsp; {ts}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="no-threat">ALL CLEAR — No threats detected in current dataset</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Logs Table ──
    st.markdown('<div class="section-header">Request Log</div>', unsafe_allow_html=True)
    if logs:
        df_table = pd.DataFrame(logs)
        df_table["anomaly"] = df_table["is_anomaly"].map({True: "THREAT", False: "CLEAN"})
        df_table["timestamp"] = df_table["timestamp"].astype(str).str[:19].str.replace("T", " ")
        st.dataframe(
            df_table[[
                "timestamp", "ip_address", "endpoint",
                "status_code", "response_time_ms",
                "request_count_last_minute", "failed_attempts",
                "anomaly", "threat_type"
            ]].rename(columns={
                "timestamp": "TIME",
                "ip_address": "IP ADDRESS",
                "endpoint": "ENDPOINT",
                "status_code": "STATUS",
                "response_time_ms": "LATENCY (ms)",
                "request_count_last_minute": "REQ/MIN",
                "failed_attempts": "FAILURES",
                "anomaly": "VERDICT",
                "threat_type": "THREAT TYPE"
            }),
            use_container_width=True,
            height=320,
            hide_index=True
        )

except requests.exceptions.ConnectionError:
    st.markdown("""
    <div style="background:#0d1117; border:1px solid #1e2d3d; border-left:3px solid #ef4444;
                border-radius:4px; padding:20px 24px; font-family:'IBM Plex Mono',monospace;">
        <div style="color:#ef4444; font-size:12px; letter-spacing:1px; font-weight:600;">
            CONNECTION ERROR
        </div>
        <div style="color:#475569; font-size:12px; margin-top:8px;">
            FastAPI server not reachable at http://127.0.0.1:8000<br>
            Make sure your backend is running: uvicorn backend.main:app --reload
        </div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")

# Auto refresh
if auto_refresh:
    time.sleep(5)
    st.rerun()