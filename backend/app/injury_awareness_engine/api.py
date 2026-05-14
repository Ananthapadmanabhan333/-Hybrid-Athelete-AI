from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from .schemas import InjuryReportIn, injuryReportOut, AdaptedPlanOut
from .services import InjuryAwarenessService
from app.models.user import User

router = APIRouter()

@router.post("/report", response_model=injuryReportOut)
def report_injury(
    report_in: InjuryReportIn,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return InjuryAwarenessService.report_injury(db, current_user.id, report_in)

@router.get("/adapted-plan", response_model=AdaptedPlanOut)
def get_adapted_plan(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return InjuryAwarenessService.get_adapted_plan(db, current_user.id)

@router.get("/status", response_model=List[injuryReportOut])
def get_injury_status(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return db.query(InjuryReport).filter(InjuryReport.user_id == current_user.id).all()
