from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.training import TrainingSession
from app.schemas.training import TrainingSessionCreate, TrainingSession as TrainingSessionSchema

router = APIRouter()

@router.post("/", response_model=TrainingSessionSchema)
def create_training_session(
    *,
    db: Session = Depends(deps.get_db),
    session_in: TrainingSessionCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Log a new training session.
    """
    db_obj = TrainingSession(
        **session_in.model_dump(),
        user_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[TrainingSessionSchema])
def read_training_sessions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve training sessions.
    """
    sessions = db.query(TrainingSession).filter(
        TrainingSession.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return sessions
