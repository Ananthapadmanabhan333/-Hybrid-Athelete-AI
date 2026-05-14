
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class BodyWeightLog(Base):
    __tablename__ = "body_weight_logs_v2" 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    weight = Column(Float) # kg
    body_fat_percentage = Column(Float, nullable=True)
    muscle_mass_estimate = Column(Float, nullable=True) 

class BodyProgressSummary(Base):
    __tablename__ = "body_progress_summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Integer)
    year = Column(Integer)
    
    start_weight = Column(Float)
    end_weight = Column(Float)
    total_weight_change = Column(Float)
    
    estimated_muscle_gain = Column(Float, default=0.0)
    estimated_fat_gain = Column(Float, default=0.0)
    estimated_fat_loss = Column(Float, default=0.0)
    
    avg_calorie_surplus_deficit = Column(Integer, default=0) # Monthly avg
