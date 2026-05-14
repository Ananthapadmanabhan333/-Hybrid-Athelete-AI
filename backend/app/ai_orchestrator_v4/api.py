from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from .services import AIOrchestratorService
from app.models.user import User

router = APIRouter()


@router.get("/dashboard-payload")
def get_dashboard_payload(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    return AIOrchestratorService.get_unified_dashboard_payload(db, current_user.id)


@router.get("/summary")
def get_performance_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Lightweight summary endpoint for the PerformanceScreen.

    It reuses the unified dashboard payload but exposes only the
    high-level scores needed by the Flutter performance UI.
    """
    payload = AIOrchestratorService.get_unified_dashboard_payload(db, current_user.id)
    return {
        "recovery_score": payload.get("recovery_score", 0),
        "adherence_pct": payload.get("adherence_pct", 0),
    }


@router.post("/validate")
def validate(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    AIOrchestratorService.run_daily_ai_validation(db, current_user.id)
    return {"status": "validated"}
