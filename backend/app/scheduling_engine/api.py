from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.scheduling_engine.schemas import (
    UserAvailabilityUpdate, UserAvailabilityOut, 
    OptimizedWeekOut, ActivitySubstitutionRequest
)
from app.scheduling_engine.services import SchedulingService
from app.models.user import User

router = APIRouter()

@router.post("/update-availability", response_model=UserAvailabilityOut)
def update_availability(
    avail_in: UserAvailabilityUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return SchedulingService.update_availability(db, current_user.id, avail_in)

@router.get("/optimized-week", response_model=OptimizedWeekOut)
def get_optimized_week(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return SchedulingService.get_optimized_week(db, current_user.id)

@router.post("/substitute", response_model=None) # Returning raw activity for now
def substitute_activity(
    request: ActivitySubstitutionRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    activity = SchedulingService.substitute_activity(db, current_user.id, request)
    if not activity:
        raise HTTPException(status_code=404, detail="Original activity not found")
    return {"message": "Activity substituted successfully", "new_activity_id": activity.id}
