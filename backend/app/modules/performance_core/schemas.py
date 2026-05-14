from pydantic import BaseModel
from datetime import date
from typing import Optional

class PerformanceSummaryBase(BaseModel):
    date: date
    month: str
    strength_score: float
    endurance_score: float
    recovery_capacity: float
    fatigue_index: float
    coach_insight_json: Optional[str] = None

class PerformanceSummaryResponse(PerformanceSummaryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
