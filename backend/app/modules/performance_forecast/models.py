
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class PerformanceForecast(Base):
    __tablename__ = "performance_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    forecast_date = Column(DateTime) # The date being forecasted for
    
    # Projections
    one_rm_bench_projection = Column(Float)
    one_rm_squat_projection = Column(Float)
    one_rm_deadlift_projection = Column(Float)
    
    body_weight_projection = Column(Float)
    
    conditioning_score_projection = Column(Float)
    
    # Metadata about the prediction (confidence, algorithm version)
    confidence_interval = Column(Float)
