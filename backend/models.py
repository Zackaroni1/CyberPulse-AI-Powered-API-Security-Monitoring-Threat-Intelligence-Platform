from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogEntry(BaseModel):
    timestamp: datetime
    ip_address: str
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    user_agent: str
    request_count_last_minute: int
    failed_attempts: int
    is_anomaly: Optional[bool] = False
    threat_type: Optional[str] = "none"