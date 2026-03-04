def classify_threat(log: dict) -> str:
    """
    Rule + ML hybrid threat classifier.
    Returns threat type based on log features.
    """
    endpoint = log.get("endpoint", "")
    status_code = log.get("status_code", 200)
    failed_attempts = log.get("failed_attempts", 0)
    request_count = log.get("request_count_last_minute", 0)
    response_time = log.get("response_time_ms", 0)
    ml_is_anomaly = log.get("ml_is_anomaly", False)

    if not ml_is_anomaly:
        return "none"

    # Rule-based classification
    if endpoint == "/api/login" and failed_attempts >= 10:
        return "brute_force"

    if request_count >= 80:
        return "bot_traffic"

    if status_code == 429 or request_count >= 50:
        return "rate_limit_violation"

    if endpoint in ["/api/admin", "/api/reset-password"] and status_code in [403, 401]:
        return "suspicious_ip"

    if response_time > 600:
        return "ddos_attempt"

    return "unknown_anomaly"