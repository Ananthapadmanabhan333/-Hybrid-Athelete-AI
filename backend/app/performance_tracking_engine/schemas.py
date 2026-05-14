from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class PerformanceMetricOut(BaseModel):
    id: int
    metric_type: str
    metric_key: str
    value: float
    unit: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True

class WearableDataIn(BaseModel):
    source: str
    data_type: str
    value: float
    metadata_json: Optional[Dict] = None

class PerformanceAnalytics(BaseModel):
    summary: Dict[str, float]
    trends: List[Dict]
    adherence_pct: float
