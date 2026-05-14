from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Dict

from app.api import deps
from app.models.user import User
from app.models.injury import Injury, InjuryStatus
from app.schemas.recovery import InjuryCreate, InjuryUpdate, InjuryResponse, RecoveryStatusResponse
from app.ai_engine.recovery_logic import RecoveryLogic

router = APIRouter()
recovery_logic = RecoveryLogic()

@router.get("/status", response_model=RecoveryStatusResponse)
def get_recovery_status(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current readiness score and recovery details.
    """
    status_data = recovery_logic.calculate_readiness(current_user, db)
    return status_data

@router.post("/injuries", response_model=InjuryResponse)
def log_injury(
    injury_in: InjuryCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Log a new injury.
    """
    injury = Injury(
        user_id=current_user.id,
        body_part=injury_in.body_part,
        injury_type=injury_in.injury_type,
        severity=injury_in.severity,
        pain_level=injury_in.pain_level,
        status=InjuryStatus.ACTIVE,
        notes=injury_in.notes
    )
    db.add(injury)
    db.commit()
    db.refresh(injury)
    return injury

@router.get("/injuries", response_model=List[InjuryResponse])
def get_active_injuries(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all active injuries.
    """
    try:
        injuries = db.query(Injury).filter(
            Injury.user_id == current_user.id,
            Injury.status != InjuryStatus.HEALED.value
        ).all()
        return injuries
    except Exception as e:
        print(f"Error fetching injuries: {e}")
        return []

@router.put("/injuries/{id}", response_model=InjuryResponse)
def update_injury(
    id: int,
    injury_in: InjuryUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update injury status (e.g., mark as healed or update pain level).
    """
    injury = db.query(Injury).filter(Injury.id == id, Injury.user_id == current_user.id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    if injury_in.pain_level is not None:
        injury.pain_level = injury_in.pain_level
    if injury_in.status is not None:
        injury.status = injury_in.status
    if injury_in.notes is not None:
        injury.notes = injury_in.notes
        
    db.commit()
    db.refresh(injury)
    return injury
