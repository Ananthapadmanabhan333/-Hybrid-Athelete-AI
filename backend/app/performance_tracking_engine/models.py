from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class PerformanceMetric(Base):
    __tablename__ = "performance_metricsv2" # v2 to avoid conflicts if any
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    metric_type = Column(String, nullable=False) # strength, endurance, mobility, volume
    metric_key = Column(String, nullable=False) # e.g. "bench_press_1rm", "squat_volume", "run_pace"
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class WearableData(Base):
    """
    Stores raw or semi-processed wearable data.
    """
    __tablename__ = "wearable_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    source = Column(String) # e.g. "applehealth", "garmin", "whoop"
    data_type = Column(String) # heart_rate, steps, calories_burned, sleep_score
    
    value = Column(Float)
    metadata_json = Column(JSON, nullable=True) # For detailed samples
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
