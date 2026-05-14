
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class PerformanceScoreBase(BaseModel):
    readiness_score: float
    hybrid_balance_score: float
    fatigue_index: float
    injury_risk: float
    details: Optional[Dict[str, Any]] = None

class PerformanceScoreCreate(PerformanceScoreBase):
    pass

class PerformanceScore(PerformanceScoreBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

class BiometricDataPoint(BaseModel):
    metric_type: str
    value: float
    source: str
    timestamp: Optional[datetime] = None

class TrendResponse(BaseModel):
    dates: List[datetime]
    scores: List[float]
    trend_direction: str # 'up', 'down', 'stable'
