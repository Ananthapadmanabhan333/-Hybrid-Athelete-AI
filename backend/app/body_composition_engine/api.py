from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import schemas, services
from app.models.user import User

router = APIRouter()

@router.get("/composition-summary", response_model=schemas.BodyCompositionSummary)
def get_composition_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    summary = services.BodyCompService.get_summary(db, current_user.id)
    if not summary:
        return {
            "lean_mass": 0, "fat_mass": 0, "body_fat_pct": 0, 
            "bulk_quality": 0, "cut_quality": 0, "waist_ratio": 0, 
            "timestamp": datetime.utcnow()
        }
    return summary
