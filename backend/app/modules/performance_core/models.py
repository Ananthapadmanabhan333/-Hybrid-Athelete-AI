from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Index
from app.db.base import Base

class PerformanceSummary(Base):
    __tablename__ = "performance_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    month = Column(String(7), nullable=False) # Format: YYYY-MM
    
    strength_score = Column(Float, default=0.0)
    endurance_score = Column(Float, default=0.0)
    recovery_capacity = Column(Float, default=100.0)
    fatigue_index = Column(Float, default=0.0)
    
    coach_insight_json = Column(String, nullable=True) 
    
    __table_args__ = (
        Index('ix_performance_summaries_user_date', 'user_id', 'date'),
        Index('ix_performance_summaries_user_month', 'user_id', 'month')
    )
