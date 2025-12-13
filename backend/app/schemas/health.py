"""
Schemas de Health Check
"""

from datetime import datetime

from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Health check da API"""

    status: str
    environment: str
    version: str
    database: str
    timestamp: datetime
