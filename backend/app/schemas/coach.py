from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class CoachInteractionRequest(BaseModel):
    fatigue_level: int # 1-10
    soreness: List[str] = [] # List of body parts
    motivation: int # 1-10
    last_night_sleep_hours: float
    message: Optional[str] = None # Optional natural language input

class CoachResponse(BaseModel):
    recommendation: str
    adjusted_plan: Optional[Dict[str, Any]] = None
    warning: Optional[str] = None
