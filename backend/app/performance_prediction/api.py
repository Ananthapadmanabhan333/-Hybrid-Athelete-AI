from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from . import schemas, services
from app.models.user import User
from typing import List

router = APIRouter()

@router.get("/predict", response_model=List[schemas.ProjectionOut])
def get_prediction(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return services.PredictionService.get_projections(db, current_user.id)

@router.get("/plateau-status", response_model=schemas.PlateauStatusOut)
def get_plateau_status(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return services.PredictionService.check_plateaus(db, current_user.id)
