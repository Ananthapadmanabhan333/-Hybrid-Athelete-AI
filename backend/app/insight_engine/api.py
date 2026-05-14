from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import services
from app.models.user import User

router = APIRouter()

@router.get("/weekly-report")
def get_weekly_report(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return services.InsightEngine.generate_weekly_report(db, current_user.id)
