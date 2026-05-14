from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class TrainingBlockOverride(Base):
    __tablename__ = "training_block_overrides"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    block_name = Column(String) # e.g. "Hypertrophy Phase 1"
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    constraints = Column(JSON) # e.g. {"max_rpe": 8, "focus": "Upper body"}
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MonthlyReport(Base):
    __tablename__ = "monthly_performance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    month_year = Column(String) # "02-2026"
    summary_text = Column(String)
    data_payload = Column(JSON)
    
    pdf_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
