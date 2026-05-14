
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session
from app.api import deps
from . import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/log", response_model=schemas.DailyHabitLog)
def log_habit(
    *,
    db: Session = Depends(deps.get_db),
    log_in: schemas.DailyHabitLogCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Log a daily habit.
    """
    log = models.DailyHabitLog(
        user_id=current_user.id,
        date=datetime.utcnow(),
        **log_in.dict()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # Update streak logic would go here
    
    return log

@router.get("/streaks", response_model=List[schemas.HabitStreak])
def get_streaks(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get all habit streaks.
    """
    streaks = db.query(models.HabitStreak).filter(
        models.HabitStreak.user_id == current_user.id
    ).all()
    return streaks
