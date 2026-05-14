from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class UserAvailabilityBase(BaseModel):
    available_slots: Dict[str, List[int]]
    compression_strategy: str = "reduce_sets"

class UserAvailabilityUpdate(UserAvailabilityBase):
    pass

class UserAvailabilityOut(UserAvailabilityBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class OptimizedWeekOut(BaseModel):
    week_start: datetime
    schedule: List[Dict] # List of activities per day

class ActivitySubstitutionRequest(BaseModel):
    activity_id: int
    new_activity_type: str
    duration_minutes: int
