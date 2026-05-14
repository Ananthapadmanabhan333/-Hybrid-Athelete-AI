
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class MicronutrientLogBase(BaseModel):
    nutrient_name: str
    amount: float
    unit: str
    source_food_id: Optional[str] = None

class MicronutrientLogCreate(MicronutrientLogBase):
    pass

class MicronutrientLog(MicronutrientLogBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True

class NutritionPlanBase(BaseModel):
    daily_calories_target: int
    protein_target: int
    carbs_target: int
    fats_target: int
    meal_plan_data: Optional[Dict] = None

class NutritionPlanCreate(NutritionPlanBase):
    pass

class NutritionPlan(NutritionPlanBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MonthlyNutritionGoalBase(BaseModel):
    month: datetime
    monthly_calorie_target: int
    current_monthly_calories: int = 0
    projected_weight_change: Optional[float] = None
    status: str = "active"

class MonthlyNutritionGoalCreate(MonthlyNutritionGoalBase):
    pass

class MonthlyNutritionGoal(MonthlyNutritionGoalBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
