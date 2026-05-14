
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class RecoveryScore(Base):
    __tablename__ = "recovery_scores"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    sleep_debt = Column(Float)
    hrv_trend = Column(Float)
    stress_score = Column(Float)
    recovery_index = Column(Float)
    
    # New detailed metrics for v2
    sleep_quality = Column(Integer) # 1-10
    resting_heart_rate = Column(Integer)
    soreness = Column(Integer) # 1-10
    stress = Column(Integer) # 1-10
    hydration_level = Column(Integer) # 1-10 or ml? Input says 1-10 implies score/feeling, but logical is ml. Stick to spec "hydration_level".
    mood = Column(String)
    cold_exposure_minutes = Column(Integer, default=0)
    sauna_minutes = Column(Integer, default=0)
    mobility_minutes = Column(Integer, default=0)

    # Sleep specific data
    total_sleep_minutes = Column(Integer)
    deep_sleep_minutes = Column(Integer)
    rem_sleep_minutes = Column(Integer)
