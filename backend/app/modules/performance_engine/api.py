
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session
from app.api import deps
from . import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/daily-log", response_model=schemas.PerformanceScore)
def create_performance_score(
    *,
    db: Session = Depends(deps.get_db),
    score_in: schemas.PerformanceScoreCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create a new daily performance score.
    """
    # Logic to calculate scores could be here or in services.py
    # For now, simplistic CRUD
    score = models.PerformanceScore(
        user_id=current_user.id,
        date=datetime.utcnow(),
        **score_in.dict()
    )
    db.add(score)
    db.commit()
    db.refresh(score)
    return score

@router.get("/trend", response_model=List[schemas.PerformanceScore])
def get_performance_trend(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 7,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get performance scores for the last 7 days (or limit).
    """
    scores = db.query(models.PerformanceScore).filter(
        models.PerformanceScore.user_id == current_user.id
    ).order_by(models.PerformanceScore.date.desc()).offset(skip).limit(limit).all()
    return scores
