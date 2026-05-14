from pydantic import BaseModel
from datetime import date
from typing import Optional

class RecoveryLogCreate(BaseModel):
    sleep_hours: float
    sleep_quality: int
    hrv: float
    resting_heart_rate: float
    soreness: int
    stress: int
    hydration_liters: float
    notes: Optional[str] = None

class RecoveryScoreResponse(BaseModel):
    date: date
    recovery_score: float
    fatigue_flag: Optional[str] = None
    
    class Config:
        orm_mode = True
