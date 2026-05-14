
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitStreakBase(BaseModel):
    habit_type: str
    current_streak: int
    max_streak: int
    last_completed_date: Optional[datetime] = None

class HabitStreak(HabitStreakBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class DailyHabitLogBase(BaseModel):
    habit_type: str
    status: bool
    value: Optional[str] = None

class DailyHabitLogCreate(DailyHabitLogBase):
    pass

class DailyHabitLog(DailyHabitLogBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True
