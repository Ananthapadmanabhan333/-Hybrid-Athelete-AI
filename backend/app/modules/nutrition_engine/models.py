
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.base import Base

class MicronutrientLog(Base):
    __tablename__ = "micronutrient_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    nutrient_name = Column(String, index=True) # e.g., 'Vitamin D', 'Iron'
    amount = Column(Float)
    unit = Column(String) # e.g., 'mg', 'iu'
    source_food_id = Column(String, nullable=True) 

class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    daily_calories_target = Column(Integer)
    protein_target = Column(Integer)
    carbs_target = Column(Integer)
    fats_target = Column(Integer)
    
    # JSON for meal plan details
    meal_plan_data = Column(JSON)

class MonthlyNutritionGoal(Base):
    __tablename__ = "monthly_nutrition_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(DateTime) # First day of the month
    
    monthly_calorie_target = Column(Integer)
    current_monthly_calories = Column(Integer, default=0)
    
    projected_weight_change = Column(Float) # kg
    
    status = Column(String, default="active") # active, completed, failed
