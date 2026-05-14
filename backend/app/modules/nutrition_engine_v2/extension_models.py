from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class MacroLoadAdjustment(Base):
    """
    Stores macro targets that adjust based on training intensity.
    """
    __tablename__ = "macro_load_adjustments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    date = Column(DateTime, nullable=False, default=func.now())
    training_intensity = Column(String) # low, medium, high
    
    target_protein = Column(Float)
    target_carbs = Column(Float)
    target_fats = Column(Float)
    target_calories = Column(Integer)
    
    # Micronutrient targets
    micronutrient_targets = Column(JSON, nullable=True) # e.g. {"zinc": "15mg", "magnesium": "400mg"}
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class NutritionCoachMessage(Base):
    """
    Stores chat history for the LLM Nutrition Coach.
    """
    __tablename__ = "nutrition_coach_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    role = Column(String, nullable=False) # user, assistant
    content = Column(Text, nullable=False)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class UserDietaryProfile(Base):
    """
    Stores dietary restrictions and preferences.
    """
    __tablename__ = "user_dietary_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    diet_type = Column(String) # vegan, keto, paleo, etc.
    restrictions = Column(JSON, default=[]) # e.g. ["peanuts", "dairy"]
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
