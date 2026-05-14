
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.api import deps
from . import models, schemas, services
from datetime import datetime

router = APIRouter()

@router.post("/log-weight", response_model=schemas.BodyWeightLog)
def log_weight(
    *,
    db: Session = Depends(deps.get_db),
    log_in: schemas.BodyWeightLogCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    return services.BodyProgressService.log_weight(db, current_user.id, log_in)

@router.get("/charts", response_model=schemas.BodyChartsResponse)
def get_body_charts(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    return services.BodyProgressService.get_charts_data(db, current_user.id)
