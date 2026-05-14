from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.adaptive_training_engine.schemas import (
    UserWorkoutProfileCreate, UserWorkoutProfileOut, 
    AdaptiveWorkoutSessionOut, PerformanceUpdate
)
from app.adaptive_training_engine.services import AdaptiveTrainingService
from app.models.user import User

router = APIRouter()

@router.post("/profile", response_model=UserWorkoutProfileOut)
def create_or_update_profile(
    profile_in: UserWorkoutProfileCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return AdaptiveTrainingService.create_or_update_profile(db, current_user.id, profile_in)

@router.get("/profile", response_model=UserWorkoutProfileOut)
def get_profile(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    profile = AdaptiveTrainingService.get_user_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/generate", response_model=AdaptiveWorkoutSessionOut)
def generate_workout(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = AdaptiveTrainingService.generate_workout(db, current_user.id)
    if not session:
        raise HTTPException(status_code=400, detail="Could not generate workout. Check user profile.")
    return session

@router.post("/update-performance", response_model=AdaptiveWorkoutSessionOut)
def update_performance(
    update: PerformanceUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = AdaptiveTrainingService.update_performance(db, current_user.id, update)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/next-session", response_model=AdaptiveWorkoutSessionOut)
def get_next_session(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    session = AdaptiveTrainingService.get_next_session(db, current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="No upcoming sessions scheduled")
    return session
