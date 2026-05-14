from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectionOut(BaseModel):
    metric: str
    current: float
    projection_4w: float
    projection_8w: float
    trend: str # "Increasing", "Stagnant", "Decreasing"

class PlateauStatusOut(BaseModel):
    stalled_metrics: List[str]
    alert_triggered: bool
    recommendation: Optional[str] = None
