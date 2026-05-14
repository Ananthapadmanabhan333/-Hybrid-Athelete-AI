from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class InjuryReportIn(BaseModel):
    affected_area: str
    pain_level: int
    notes: Optional[str] = None

class injuryReportOut(BaseModel):
    id: int
    affected_area: str
    pain_level: int
    reported_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class AdaptedPlanOut(BaseModel):
    modified_exercises: List[Dict]
    recommendation: str
    trigger_recovery_week: bool
