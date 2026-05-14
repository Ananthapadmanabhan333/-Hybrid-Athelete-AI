
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PerformanceForecastBase(BaseModel):
    forecast_date: datetime
    one_rm_bench_projection: Optional[float] = None
    one_rm_squat_projection: Optional[float] = None
    one_rm_deadlift_projection: Optional[float] = None
    body_weight_projection: Optional[float] = None
    conditioning_score_projection: Optional[float] = None
    confidence_interval: Optional[float] = None

class PerformanceForecastCreate(PerformanceForecastBase):
    pass

class PerformanceForecast(PerformanceForecastBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
