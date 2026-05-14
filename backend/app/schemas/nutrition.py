from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.nutrition import MealType

class NutritionLogBase(BaseModel):
    food_name: str
    calories: int
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fats_g: float = 0.0
    meal_type: MealType
    timestamp: Optional[datetime] = None

class NutritionLogCreate(NutritionLogBase):
    pass

class NutritionLog(NutritionLogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class WaterLogBase(BaseModel):
    amount_ml: float
    timestamp: Optional[datetime] = None

class WaterLogCreate(WaterLogBase):
    pass

class WaterLog(WaterLogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
