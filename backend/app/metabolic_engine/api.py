from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import schemas, services
from app.models.user import User

router = APIRouter()

@router.get("/status", response_model=schemas.MetabolicStatusOut)
def get_status(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    status, label = services.MetabolicService.get_status(db, current_user.id)
    return {
        "user_id": status.user_id,
        "current_tdee": status.current_tdee,
        "adaptation_index": status.adaptation_index,
        "last_recalc_at": status.last_recalc_at,
        "status_label": label
    }

@router.post("/recalculate")
def recalculate(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    result = services.MetabolicService.recalculate_tdee(db, current_user.id)
    if not result:
        return {"error": "Insufficient data (minimum 2 weights and 7 days of logs required)"}
    return {"status": "success", "new_tdee": result.current_tdee}
