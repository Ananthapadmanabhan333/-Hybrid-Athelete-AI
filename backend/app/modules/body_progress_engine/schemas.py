
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BodyWeightLogBase(BaseModel):
    weight: float
    body_fat_percentage: Optional[float] = None
    muscle_mass_estimate: Optional[float] = None

class BodyWeightLogCreate(BodyWeightLogBase):
    pass

class BodyWeightLog(BodyWeightLogBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True

class BodyProgressSummaryBase(BaseModel):
    month: int
    year: int
    start_weight: float
    end_weight: float
    total_weight_change: float
    estimated_muscle_gain: float
    estimated_fat_gain: float
    estimated_fat_loss: float
    avg_calorie_surplus_deficit: int

class BodyProgressSummary(BodyProgressSummaryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Chart Data Point
class ChartDataPoint(BaseModel):
    date: datetime
    value: float
    secondary_value: Optional[float] = None # e.g. muscle est or surplus

class BodyChartsResponse(BaseModel):
    gain_chart: List[ChartDataPoint]
    loss_chart: List[ChartDataPoint]
    summary: Optional[BodyProgressSummary] = None
