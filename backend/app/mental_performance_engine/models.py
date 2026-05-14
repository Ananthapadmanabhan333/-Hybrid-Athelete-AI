from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class MentalState(Base):
    __tablename__ = "mental_states"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    mood_score = Column(Integer) # 1-10
    motivation_score = Column(Integer) # 1-10
    enjoyment_score = Column(Integer) # 1-10
    
    burnout_risk = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class MentalHistory(Base):
    __tablename__ = "mental_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    avg_mood = Column(Float)
    risk_trend = Column(String)
    week_start = Column(DateTime)
