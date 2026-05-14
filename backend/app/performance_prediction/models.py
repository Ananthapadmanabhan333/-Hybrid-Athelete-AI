from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class PerformanceProjection(Base):
    __tablename__ = "performance_projections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    metric_type = Column(String) # e.g. "bench_press_1rm", "vo2_max"
    current_value = Column(Float)
    projected_4w = Column(Float)
    projected_8w = Column(Float)
    
    confidence_score = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class PlateauAlert(Base):
    __tablename__ = "plateau_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    metric = Column(String)
    weeks_stalled = Column(Integer)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
