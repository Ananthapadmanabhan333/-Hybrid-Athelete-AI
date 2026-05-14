
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON
from datetime import datetime
from app.db.base import Base
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

class AthleteLevel(Base):
    __tablename__ = "athlete_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    strength_level = Column(SQLEnum(StrengthLevel), default=StrengthLevel.BEGINNER)
    boxing_level = Column(SQLEnum(BoxingLevel), default=BoxingLevel.AMATEUR)
    
    # Calculated Hybrid Level (0-100 or similar score/rank)
    hybrid_level_score = Column(Float) 
    hybrid_label = Column(String) # e.g. "Hybrid Athlete Level 3"

    # Store calculation source data (what lifts/stats caused this level)
    source_data = Column(JSON) 
