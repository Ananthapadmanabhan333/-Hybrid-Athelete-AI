from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from .schemas import PerformanceMetricOut, WearableDataIn, PerformanceAnalytics
from .services import PerformanceTrackingService
from app.models.user import User

router = APIRouter()

@router.get("/progress", response_model=PerformanceAnalytics)
def get_progress(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return PerformanceTrackingService.get_analytics(db, current_user.id)

@router.get("/analytics", response_model=PerformanceAnalytics)
def get_analytics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return PerformanceTrackingService.get_analytics(db, current_user.id)

@router.post("/wearable-sync", response_model=None)
def sync_wearable_data(
    data: WearableDataIn,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    PerformanceTrackingService.log_wearable(db, current_user.id, data)
    return {"status": "success"}

@router.get("/history", response_model=List[PerformanceMetricOut])
def get_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # This would query PerformanceMetric table
    return []
