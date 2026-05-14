from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class UserWorkoutProfileBase(BaseModel):
    goal_type: str
    current_level: int = Field(ge=1, le=10)
    available_equipment: List[str]
    weekly_schedule: Dict[str, int]
    session_duration_preference: int
    mobility_limits: List[str] = []
    injury_history: List[str] = []

class UserWorkoutProfileCreate(UserWorkoutProfileBase):
    pass

class UserWorkoutProfileUpdate(BaseModel):
    goal_type: Optional[str] = None
    current_level: Optional[int] = None
    available_equipment: Optional[List[str]] = None
    weekly_schedule: Optional[Dict[str, int]] = None
    session_duration_preference: Optional[int] = None
    mobility_limits: Optional[List[str]] = None
    injury_history: Optional[List[str]] = None

class UserWorkoutProfileOut(UserWorkoutProfileBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class AdaptiveWorkoutSessionOut(BaseModel):
    id: int
    scheduled_date: datetime
    status: str
    workout_payload: Dict
    intensity_adjustment: float
    
    class Config:
        from_attributes = True

class PerformanceUpdate(BaseModel):
    session_id: int
    duration_minutes: int
    performance_score: float # 0.0 to 1.0
    rpe: int # 1-10
    completed_as_planned: bool
    notes: Optional[str] = None
