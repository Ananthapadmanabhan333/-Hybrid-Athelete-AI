from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class UserAvailability(Base):
    __tablename__ = "user_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Weekly slots: {"mon": [20, 45], "tue": [60], ...} where values are available minutes
    available_slots = Column(JSON, nullable=False)
    
    # Preferred compression strategy: "reduce_sets", "remove_accessory", "increase_intensity"
    compression_strategy = Column(String, default="reduce_sets")
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="availability_link")

class ScheduledActivity(Base):
    __tablename__ = "scheduled_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    activity_type = Column(String, nullable=False) # "workout", "hiking", "cycling", "recovery"
    scheduled_for = Column(DateTime, nullable=False)
    planned_duration_minutes = Column(Integer, nullable=False)
    
    is_substituted = Column(Boolean, default=False)
    original_activity_id = Column(Integer, nullable=True) # If this replaced something else
    
    status = Column(String, default="scheduled") # scheduled, completed, missed, moved
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="scheduled_activities")
