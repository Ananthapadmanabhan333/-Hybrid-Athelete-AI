
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import enum

class NutritionGoalType(str, enum.Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTENANCE = "maintenance"

class MonthlyCalorieSummaryBase(BaseModel):
    month: int
    year: int
    daily_calorie_target: int
    monthly_calorie_target: int
    calories_consumed_so_far: int
    surplus_or_deficit: int
    projected_weight_change: float
    goal_type: NutritionGoalType
    
    protein_compliance_pct: float
    carb_consistency_pct: float
    hydration_adherence_pct: float
    micronutrient_score: float
    monthly_nutrition_score: float

class MonthlyCalorieSummary(MonthlyCalorieSummaryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class NutritionInsights(BaseModel):
    insights: List[str]
    actionable_tips: List[str]
    status: str # "On Track", "Needs Attention"
