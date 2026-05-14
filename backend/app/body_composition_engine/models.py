from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class BodyComposition(Base):
    __tablename__ = "body_composition"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    lean_mass = Column(Float)
    fat_mass = Column(Float)
    body_fat_pct = Column(Float)
    waist_circumference = Column(Float)
    
    waist_to_weight_ratio = Column(Float)
    
    bulk_quality_score = Column(Float)
    cut_quality_score = Column(Float)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
