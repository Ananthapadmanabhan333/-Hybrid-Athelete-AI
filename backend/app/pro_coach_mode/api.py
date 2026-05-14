from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import services
from app.models.user import User

router = APIRouter()

@router.post("/block-override")
def create_override(
    block_name: str,
    constraints: dict,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return services.ProCoachService.create_block_override(db, current_user.id, block_name, constraints)

@router.get("/monthly-report")
def get_monthly_report(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return services.ProCoachService.generate_monthly_report(db, current_user.id)
