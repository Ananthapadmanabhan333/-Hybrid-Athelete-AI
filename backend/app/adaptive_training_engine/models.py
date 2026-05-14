from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class UserWorkoutProfile(Base):
    """
    Detailed user profile for adaptive training.
    """
    __tablename__ = "user_workout_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    goal_type = Column(String, nullable=False) # muscle, fat_loss, strength, endurance, hybrid
    current_level = Column(Integer, default=1) # 1-10 scale
    available_equipment = Column(JSON, default=[]) # e.g., ["dumbbells", "barbell", "bench"]
    weekly_schedule = Column(JSON, default={}) # e.g., {"mon": 60, "tue": 0, "wed": 45} (minutes)
    session_duration_preference = Column(Integer, default=45) # preferred duration in minutes
    mobility_limits = Column(JSON, default=[]) # e.g., ["tight_shoulders", "knee_pain"]
    injury_history = Column(JSON, default=[]) # tracked for adaptation
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="workout_profile_link") # Using backref for simplicity as per rules not to modify existing files if possible

class AdaptiveWorkoutSession(Base):
    """
    Stores the generated adaptive workout sessions.
    """
    __tablename__ = "adaptive_workout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    scheduled_date = Column(DateTime, nullable=False)
    actual_start_at = Column(DateTime, nullable=True)
    actual_duration_minutes = Column(Integer, nullable=True)
    
    status = Column(String, default="scheduled") # scheduled, completed, missed, cancelled
    intensity_adjustment = Column(Float, default=1.0) # multiplier applied based on recovery/performance
    
    workout_payload = Column(JSON, nullable=False) # The actual exercises, sets, reps generated
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="adaptive_sessions")
