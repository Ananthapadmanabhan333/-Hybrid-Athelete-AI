
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .models import RecoveryMethodType

# Log Schemas
class RecoveryLogV3Base(BaseModel):
    sleep_duration: float
    sleep_quality: int # 1-10
    hrv: int
    resting_heart_rate: int
    muscle_soreness: int # 1-10
    stress_level: int # 1-10
    hydration_liters: float
    mood: Optional[str] = None
    notes: Optional[str] = None

class RecoveryLogV3Create(RecoveryLogV3Base):
    pass

class RecoveryLogV3(RecoveryLogV3Base):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        from_attributes = True

# Method Schemas
class RecoveryMethodLogBase(BaseModel):
    method_type: RecoveryMethodType
    duration_minutes: int
    notes: Optional[str] = None

class RecoveryMethodLogCreate(RecoveryMethodLogBase):
    pass

class RecoveryMethodLog(RecoveryMethodLogBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True

# Score Schemas
class RecoveryScoreV3(BaseModel):
    id: int
    user_id: int
    date: datetime
    total_score: float
    category: str
    
    sleep_component: float
    hrv_component: float
    rhr_component: float
    soreness_component: float
    stress_component: float
    hydration_component: float

    class Config:
        from_attributes = True

# Recommendation Schemas
class RecoveryRecommendation(BaseModel):
    id: int
    recommendation_text: str
    type: str
    priority: int

    class Config:
        from_attributes = True

# Aggregated Response
class RecoveryDailySummary(BaseModel):
    date: datetime
    score: Optional[RecoveryScoreV3] = None
    logs: List[RecoveryLogV3] = []
    methods: List[RecoveryMethodLog] = []
    recommendations: List[RecoveryRecommendation] = []
