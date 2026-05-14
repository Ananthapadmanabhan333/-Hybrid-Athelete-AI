from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class MacroAdjustmentOut(BaseModel):
    date: datetime
    training_intensity: str
    target_protein: float
    target_carbs: float
    target_fats: float
    target_calories: int
    micronutrient_targets: Optional[Dict[str, str]] = None
    
    class Config:
        from_attributes = True

class NutritionCoachChatRequest(BaseModel):
    message: str

class NutritionCoachChatResponse(BaseModel):
    reply: str
    suggested_macros: Optional[MacroAdjustmentOut] = None

class UserDietaryProfileBase(BaseModel):
    diet_type: str
    restrictions: List[str]

class UserDietaryProfileUpdate(UserDietaryProfileBase):
    pass

class UserDietaryProfileOut(UserDietaryProfileBase):
    user_id: int
    
    class Config:
        from_attributes = True
