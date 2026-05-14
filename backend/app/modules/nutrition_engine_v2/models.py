
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from datetime import datetime
from app.db.base import Base
import enum

class NutritionGoalType(str, enum.Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTENANCE = "maintenance"

class MonthlyCalorieSummary(Base):
    __tablename__ = "monthly_calorie_summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Integer) # 1-12
    year = Column(Integer) 
    
    daily_calorie_target = Column(Integer)
    monthly_calorie_target = Column(Integer) # daily * days_in_month
    calories_consumed_so_far = Column(Integer, default=0)
    
    # Calculated fields
    surplus_or_deficit = Column(Integer, default=0) # + for surplus, - for deficit
    projected_weight_change = Column(Float, default=0.0) # kg
    
    goal_type = Column(SQLEnum(NutritionGoalType), default=NutritionGoalType.MAINTENANCE)
    
    # Adherence metrics
    protein_compliance_pct = Column(Float, default=0.0)
    carb_consistency_pct = Column(Float, default=0.0)
    hydration_adherence_pct = Column(Float, default=0.0)
    micronutrient_score = Column(Float, default=0.0)
    
    monthly_nutrition_score = Column(Float, default=0.0) # The composite score
