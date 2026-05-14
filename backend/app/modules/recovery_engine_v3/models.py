
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from datetime import datetime
from app.db.base import Base
import enum

class RecoveryMethodType(str, enum.Enum):
    COLD_EXPOSURE = "cold"
    SAUNA = "sauna"
    MOBILITY = "mobility"
    MASSAGE = "massage"
    ACTIVE_RECOVERY = "active_recovery"

class RecoveryLogV3(Base):
    __tablename__ = "recovery_logs_v3"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Core Metrics
    sleep_duration = Column(Float) # hours
    sleep_quality = Column(Integer) # 1-10
    hrv = Column(Integer) # milliseconds
    resting_heart_rate = Column(Integer) # bpm
    muscle_soreness = Column(Integer) # 1-10 (10 is extremely sore)
    stress_level = Column(Integer) # 1-10
    hydration_liters = Column(Float)
    mood = Column(String) # e.g. "Great", "Tired", "Stressed"
    notes = Column(Text, nullable=True)

class RecoveryMethodLog(Base):
    __tablename__ = "recovery_method_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    method_type = Column(SQLEnum(RecoveryMethodType))
    duration_minutes = Column(Integer)
    notes = Column(Text, nullable=True)

class RecoveryScoreV3(Base):
    __tablename__ = "recovery_scores_v3"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    total_score = Column(Float)
    category = Column(String) # Elite, Ready, Moderate, Reduce
    
    # Breakdowns for UI visualization
    sleep_component = Column(Float)
    hrv_component = Column(Float)
    rhr_component = Column(Float)
    soreness_component = Column(Float)
    stress_component = Column(Float)
    hydration_component = Column(Float)

class RecoveryRecommendation(Base):
    __tablename__ = "recovery_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    recommendation_text = Column(String)
    type = Column(String) # hydration, mobility, intensity, rest
    priority = Column(Integer) # 1 (High) - 3 (Low)
