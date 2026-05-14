from datetime import date
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.modules.performance_core.models import PerformanceSummary
from app.modules.performance_core.schemas import PerformanceSummaryResponse
from app.modules.performance_core.services import compute_daily_performance

router = APIRouter()

@router.get("/summary/daily", response_model=PerformanceSummaryResponse)
def get_daily_summary(
    target_date: date,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Fetch pre-computed dashboard metrics in 1 query."""
    summary = db.query(PerformanceSummary).filter(
        PerformanceSummary.user_id == current_user.id,
        PerformanceSummary.date == target_date
    ).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not computed for this date")
        
    return summary

@router.post("/jobs/trigger-compute")
def trigger_compute_job(
    target_date: date,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Background computation of deterministic performance scores."""
    background_tasks.add_task(compute_daily_performance, current_user.id, target_date, db)
    return {"status": "Job queued"}
