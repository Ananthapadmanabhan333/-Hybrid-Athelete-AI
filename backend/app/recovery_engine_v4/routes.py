from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.api import deps
from app.models.user import User
from app.recovery_engine_v4.models import RecoveryScore
from app.recovery_engine_v4.schemas import RecoveryLogCreate, RecoveryScoreResponse
from app.recovery_engine_v4.services import save_recovery_log_and_compute

router = APIRouter()

@router.post("/log", response_model=RecoveryScoreResponse)
async def create_recovery_log(
    payload: RecoveryLogCreate,
    target_date: date = date.today(),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    if payload.sleep_quality < 1 or payload.sleep_quality > 10:
        raise HTTPException(status_code=422, detail="Sleep quality must be 1-10")
        
    score = save_recovery_log_and_compute(payload, current_user.id, target_date, db)
    return score

@router.get("/today", response_model=RecoveryScoreResponse)
async def get_today_recovery(
    target_date: date = date.today(),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    score = db.query(RecoveryScore).filter(
        RecoveryScore.user_id == current_user.id,
        RecoveryScore.date == target_date
    ).first()
    
    if not score:
        raise HTTPException(status_code=404, detail="No recovery log found for today")
        
    return score
