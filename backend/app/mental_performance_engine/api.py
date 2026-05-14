from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import schemas, services
from app.models.user import User

router = APIRouter()

@router.get("/status", response_model=schemas.MentalStatusOut)
def get_mental_status(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    status = services.MentalService.get_status(db, current_user.id)
    if not status:
        return {"mood": 0, "motivation": 0, "burnout_risk": 0.0, "recommendation": "No data logged yet."}
    return status

@router.post("/log")
def log_mental_state(
    log_in: schemas.MentalLogIn,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    services.MentalService.log_state(
        db, current_user.id, log_in.mood, log_in.motivation, log_in.enjoyment
    )
    return {"status": "Mental state logged."}
