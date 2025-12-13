"""
Schemas de Health Check
"""
from pydantic import BaseModel
from datetime import datetime


class HealthCheck(BaseModel):
    """Health check da API"""
    status: str
    environment: str
    version: str
    database: str
    timestamp: datetime
