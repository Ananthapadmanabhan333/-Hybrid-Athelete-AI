from datetime import date
from typing import Optional
from pydantic import BaseModel

class DailyLogBase(BaseModel):
    date: Optional[date] = None
    total_calories_in: int = 0
    total_training_minutes: int = 0
    recovery_score: int = 0
    sleep_hours: float = 0.0
    mood: Optional[int] = None
    soreness_level: Optional[int] = None
    notes: Optional[str] = None

class DailyLogCreate(DailyLogBase):
    date: date

class DailyLogUpdate(DailyLogBase):
    pass

class DailyLog(DailyLogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
