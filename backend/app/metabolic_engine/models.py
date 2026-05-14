from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class MetabolicStatus(Base):
    __tablename__ = "metabolic_status"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    current_tdee = Column(Float, default=2500.0)
    bmr = Column(Float)
    adaptation_index = Column(Float, default=1.0) # 1.0 is healthy, < 0.8 is slowing
    
    rolling_14d_weight_avg = Column(Float)
    expected_weight_change = Column(Float)
    actual_weight_change = Column(Float)
    
    last_recalc_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class MetabolicLog(Base):
    __tablename__ = "metabolic_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tdee_estimate = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
