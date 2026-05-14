
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.api import deps
from . import schemas
from app.models.user import User

# Import other module models for aggregation
from app.modules.performance_engine import models as perf_models
from app.modules.recovery_engine import models as rec_models
from app.modules.athlete_level_engine import models as level_models
from app.modules.nutrition_engine import models as nut_models

router = APIRouter()

@router.get("/overview", response_model=schemas.DashboardOverview)
def get_dashboard_overview(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    # 1. Fetch latest data
    perf = db.query(perf_models.PerformanceScore).filter(perf_models.PerformanceScore.user_id == current_user.id).order_by(perf_models.PerformanceScore.date.desc()).first()
    rec = db.query(rec_models.RecoveryScore).filter(rec_models.RecoveryScore.user_id == current_user.id).order_by(rec_models.RecoveryScore.date.desc()).first()
    level = db.query(level_models.AthleteLevel).filter(level_models.AthleteLevel.user_id == current_user.id).first()
    
    # Defaults
    readiness = perf.readiness_score if perf else 0.0
    recovery = rec.recovery_index if rec else 0.0
    
    # Nutrition defaults (mock logic for "remaining")
    cal_remaining = 500 
    prot_remaining = 30
    hydro_remaining = 1000
    
    # FUELIX Score Calculation
    # (TrainingProgress * 0.4) + (RecoveryIndex * 0.2) + (NutritionAdherence * 0.2) + (HealthStability * 0.2)
    training_progress = 80.0 # Mock: Derive from workout volume trend
    nutrition_adherence = 85.0 # Mock
    health_stability = 90.0 # Mock: Derive from lab flags/symptoms
    
    fuelix_score = (training_progress * 0.4) + (recovery * 0.2) + (nutrition_adherence * 0.2) + (health_stability * 0.2)
    
    return schemas.DashboardOverview(
        fuelix_score=fuelix_score,
        readiness_score=readiness,
        recovery_score=recovery,
        calories_remaining=cal_remaining,
        protein_remaining=prot_remaining,
        hydration_remaining_ml=hydro_remaining,
        today_training_intensity="Medium",
        ai_priority_action="Prioritize sleep tonight to boost recovery.",
        strength_level=level.strength_level.value if level else "Beginner",
        boxing_level=level.boxing_level.value if level else "Amateur",
        hybrid_level=level.hybrid_label if level and level.hybrid_label else "Level 1",
        fatigue_warning=False,
        lab_flags=0,
        nutrition_adjustment_suggestion="Incresase carbs post-workout."
    )
