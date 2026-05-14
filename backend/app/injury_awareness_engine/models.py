from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class InjuryReport(Base):
    __tablename__ = "injury_reports_v2"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    affected_area = Column(String, nullable=False) # e.g. "left_shoulder", "lower_back"
    pain_level = Column(Integer) # 1-10
    reported_at = Column(DateTime(timezone=True), server_default=func.now())
    
    is_active = Column(Boolean, default=True)
    notes = Column(String)
    
    # Flags for automated logic
    requires_substitution = Column(Boolean, default=True)
    requires_deload = Column(Boolean, default=False)

class MobilityConstraint(Base):
    __tablename__ = "mobility_constraints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    joint = Column(String, nullable=False) # e.g. "ankle", "shoulder"
    constraint_type = Column(String) # e.g. "dorsiflexion_limit", "internal_rotation_limit"
    severity = Column(Integer) # 1-5
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
