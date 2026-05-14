
from pydantic import BaseModel
from typing import Optional, List, Any

# Dashboard aggregate response
class DashboardOverview(BaseModel):
    fuelix_score: float
    
    # Legacy/Existing Metrics
    readiness_score: float
    recovery_score: float
    
    # Nutrition
    calories_remaining: int
    protein_remaining: int
    hydration_remaining_ml: int
    
    # Training
    today_training_intensity: str # Low, Medium, High
    ai_priority_action: str
    
    # Levels (from Athlete Level Engine)
    strength_level: str
    boxing_level: str
    hybrid_level: str
    
    # Flags
    fatigue_warning: bool
    lab_flags: int # count
    nutrition_adjustment_suggestion: Optional[str] = None

class FuelixScoreBreakdown(BaseModel):
    training_progress: float
    recovery_index: float
    nutrition_adherence: float
    health_stability: float
    total_score: float
