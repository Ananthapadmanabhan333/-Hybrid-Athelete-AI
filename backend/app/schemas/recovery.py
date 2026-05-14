from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.injury import BodyPart, InjuryType, InjuryStatus

class InjuryBase(BaseModel):
    body_part: BodyPart
    injury_type: InjuryType
    severity: str
    pain_level: int
    notes: Optional[str] = None

class InjuryCreate(InjuryBase):
    pass

class InjuryUpdate(BaseModel):
    pain_level: Optional[int] = None
    status: Optional[InjuryStatus] = None
    notes: Optional[str] = None

class InjuryResponse(InjuryBase):
    id: int
    user_id: int
    status: InjuryStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RecoveryStatusResponse(BaseModel):
    score: int
    status: str
    breakdown: List[str]
    active_injuries: List[str]
