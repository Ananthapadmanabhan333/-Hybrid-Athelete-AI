
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecoveryScoreBase(BaseModel):
    sleep_debt: float
    hrv_trend: float
    stress_score: float
    recovery_index: float
    
    # v2 fields
    sleep_quality: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    soreness: Optional[int] = None
    stress: Optional[int] = None
    hydration_level: Optional[int] = None
    mood: Optional[str] = None
    cold_exposure_minutes: Optional[int] = 0
    sauna_minutes: Optional[int] = 0
    mobility_minutes: Optional[int] = 0
    
    total_sleep_minutes: Optional[int] = None
    deep_sleep_minutes: Optional[int] = None
    rem_sleep_minutes: Optional[int] = None

class RecoveryScoreCreate(RecoveryScoreBase):
    pass

class RecoveryScore(RecoveryScoreBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True
