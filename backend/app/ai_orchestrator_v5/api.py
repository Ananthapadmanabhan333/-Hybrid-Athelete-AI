from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import services
from app.models.user import User

router = APIRouter()

@router.get("/summary")
async def get_orchestrated_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return await services.AIOrchestratorV5.get_orchestrated_summary(db, current_user.id)
