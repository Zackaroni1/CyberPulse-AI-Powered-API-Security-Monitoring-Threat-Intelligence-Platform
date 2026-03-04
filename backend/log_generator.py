import random
from datetime import datetime
from faker import Faker

fake = Faker()

ENDPOINTS = [
    "/api/login",
    "/api/register",
    "/api/payment",
    "/api/profile",
    "/api/dashboard",
    "/api/admin",
    "/api/reset-password"
]

NORMAL_IPS = [fake.ipv4() for _ in range(20)]
SUSPICIOUS_IPS = [fake.ipv4() for _ in range(5)]

def generate_normal_log():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": random.choice(NORMAL_IPS),
        "endpoint": random.choice(ENDPOINTS[:5]),  # normal endpoints
        "method": random.choice(["GET", "POST"]),
        "status_code": random.choices([200, 201, 204], weights=[70, 20, 10])[0],
        "response_time_ms": round(random.uniform(50, 300), 2),
        "user_agent": fake.user_agent(),
        "request_count_last_minute": random.randint(1, 10),
        "failed_attempts": random.randint(0, 1),
        "is_anomaly": False,
        "threat_type": "none"
    }

def generate_attack_log(attack_type="brute_force"):
    base = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": random.choice(SUSPICIOUS_IPS),
        "method": "POST",
        "user_agent": fake.user_agent(),
        "is_anomaly": True,
    }

    if attack_type == "brute_force":
        base.update({
            "endpoint": "/api/login",
            "status_code": 401,
            "response_time_ms": round(random.uniform(200, 500), 2),
            "request_count_last_minute": random.randint(40, 100),
            "failed_attempts": random.randint(10, 50),
            "threat_type": "brute_force"
        })
    elif attack_type == "bot_traffic":
        base.update({
            "endpoint": random.choice(ENDPOINTS),
            "status_code": 200,
            "response_time_ms": round(random.uniform(10, 50), 2),
            "request_count_last_minute": random.randint(80, 200),
            "failed_attempts": 0,
            "threat_type": "bot_traffic"
        })
    elif attack_type == "rate_limit":
        base.update({
            "endpoint": "/api/payment",
            "status_code": 429,
            "response_time_ms": round(random.uniform(100, 300), 2),
            "request_count_last_minute": random.randint(50, 150),
            "failed_attempts": random.randint(5, 20),
            "threat_type": "rate_limit_violation"
        })
    elif attack_type == "suspicious_ip":
        base.update({
            "endpoint": "/api/admin",
            "status_code": 403,
            "response_time_ms": round(random.uniform(300, 800), 2),
            "request_count_last_minute": random.randint(20, 60),
            "failed_attempts": random.randint(3, 15),
            "threat_type": "suspicious_ip"
        })

    return base

def generate_log_batch(total=20, attack_ratio=0.2):
    logs = []
    attack_count = int(total * attack_ratio)
    normal_count = total - attack_count

    for _ in range(normal_count):
        logs.append(generate_normal_log())

    attack_types = ["brute_force", "bot_traffic", "rate_limit", "suspicious_ip"]
    for _ in range(attack_count):
        logs.append(generate_attack_log(random.choice(attack_types)))

    random.shuffle(logs)
    return logs