
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import enum

class StrengthLevel(str, enum.Enum):
    BEGINNER = "Beginner"
    NOVICE = "Novice"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ELITE = "Elite"

class BoxingLevel(str, enum.Enum):
    AMATEUR = "Amateur"
    CLUB_FIGHTER = "Club Fighter"
    ADVANCED = "Advanced"
    ELITE = "Elite"
    PRO = "Pro"

class AthleteLevelBase(BaseModel):
    strength_level: StrengthLevel = StrengthLevel.BEGINNER
    boxing_level: BoxingLevel = BoxingLevel.AMATEUR
    hybrid_level_score: Optional[float] = None
    hybrid_label: Optional[str] = None
    source_data: Optional[Any] = None

class AthleteLevelCreate(AthleteLevelBase):
    pass

class AthleteLevel(AthleteLevelBase):
    id: int
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True
