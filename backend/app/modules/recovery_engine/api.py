
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session
from app.api import deps
from . import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/daily-log", response_model=schemas.RecoveryScore)
def create_recovery_score(
    *,
    db: Session = Depends(deps.get_db),
    score_in: schemas.RecoveryScoreCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Log daily recovery stats and calculate Recovery Score.
    """
    
    # Simple normalization logic (Placeholder for complex statistical normalization)
    sleep_score = (score_in.sleep_quality or 5) * 10 # Scale to 100
    hrv_score = min(score_in.hrv_trend * 10, 100) # Assuming trend is raw ms or similar, need real baseline logic
    # Simplified for prototype:
    hrv_score = 70 # Mock baseline
    
    # Calculate components
    comp_sleep = (score_in.sleep_quality or 5) * 10 * 0.25
    comp_hrv = hrv_score * 0.2
    comp_rhr = 80 * 0.15 # Mock stability
    comp_soreness = ((10 - (score_in.soreness or 5)) * 10) * 0.15
    comp_stress = ((10 - (score_in.stress or 5)) * 10) * 0.15
    comp_hydration = (score_in.hydration_level or 5) * 10 * 0.1
    
    final_score = comp_sleep + comp_hrv + comp_rhr + comp_soreness + comp_stress + comp_hydration
    
    # Create DB Object
    db_obj = models.RecoveryScore(
        user_id=current_user.id,
        date=datetime.utcnow(),
        sleep_debt=score_in.sleep_debt,
        hrv_trend=score_in.hrv_trend,
        stress_score=score_in.stress_score,
        recovery_index=final_score, # Overwriting with new calculated score
        
        sleep_quality=score_in.sleep_quality,
        resting_heart_rate=score_in.resting_heart_rate,
        soreness=score_in.soreness,
        stress=score_in.stress,
        hydration_level=score_in.hydration_level,
        mood=score_in.mood,
        cold_exposure_minutes=score_in.cold_exposure_minutes,
        sauna_minutes=score_in.sauna_minutes,
        mobility_minutes=score_in.mobility_minutes,
        
        total_sleep_minutes=score_in.total_sleep_minutes,
        deep_sleep_minutes=score_in.deep_sleep_minutes,
        rem_sleep_minutes=score_in.rem_sleep_minutes
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/trend", response_model=List[schemas.RecoveryScore])
def get_recovery_trend(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 7,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get recovery scores for the last 7 days.
    """
    scores = db.query(models.RecoveryScore).filter(
        models.RecoveryScore.user_id == current_user.id
    ).order_by(models.RecoveryScore.date.desc()).offset(skip).limit(limit).all()
    return scores
