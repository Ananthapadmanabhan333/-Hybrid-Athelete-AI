
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class PerformanceScore(Base):
    __tablename__ = "performance_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    readiness_score = Column(Float)
    hybrid_balance_score = Column(Float)
    fatigue_index = Column(Float)
    injury_risk = Column(Float)
    
    # Store detailed breakdown if needed
    details = Column(JSON, nullable=True)

class BiometricTimeSeries(Base):
    __tablename__ = "biometric_timeseries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metric_type = Column(String, index=True) # e.g., 'heart_rate', 'steps', 'calories'
    value = Column(Float)
    source = Column(String) # e.g., 'apple_health', 'manual'
