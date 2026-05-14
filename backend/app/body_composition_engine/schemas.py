from pydantic import BaseModel
from datetime import datetime

class BodyCompositionSummary(BaseModel):
    lean_mass: float
    fat_mass: float
    body_fat_pct: float
    bulk_quality: float
    cut_quality: float
    waist_ratio: float
    timestamp: datetime
