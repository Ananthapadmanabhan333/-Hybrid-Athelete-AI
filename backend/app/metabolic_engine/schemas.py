from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetabolicStatusOut(BaseModel):
    user_id: int
    current_tdee: float
    adaptation_index: float
    last_recalc_at: datetime
    status_label: str # "Healthy", "Slowdown", "Recovery Required"

    class Config:
        from_attributes = True

class RecalculateRequest(BaseModel):
    days_to_analyze: int = 14
