from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.training import TrainingType

class TrainingSessionBase(BaseModel):
    type: TrainingType
    started_at: Optional[datetime] = None
    duration_minutes: int
    rpe: Optional[int] = None
    load_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class TrainingSessionCreate(TrainingSessionBase):
    pass

class TrainingSessionUpdate(TrainingSessionBase):
    pass

class TrainingSession(TrainingSessionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
