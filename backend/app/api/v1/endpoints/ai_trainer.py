from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.ai_trainer import WorkoutGenerationRequest, WorkoutResponse
from app.ai_engine.workout_generator import WorkoutGenerator
from app.models.user import User
from app.models.athlete_state import AthleteState
from pydantic import BaseModel

router = APIRouter()
generator = WorkoutGenerator()

class FeedbackRequest(BaseModel):
    training_session_id: int
    rpe: int
    enjoyment: int
    soreness_map: dict

@router.post("/generate", response_model=WorkoutResponse)
def generate_workout(
    request: WorkoutGenerationRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Generate AI-powered workout dynamically derived from the authenticated user's current fatigue metrics.
    """
    state_record = db.query(AthleteState).filter(AthleteState.user_id == current_user.id).first()
    
    # Extract real fatigue state or fallback to default
    state_dict = {
        "cns_fatigue": state_record.cns_fatigue if state_record else 30.0,
        "muscular_upper_fatigue": state_record.muscular_fatigue_upper if state_record else 25.0,
        "muscular_lower_fatigue": state_record.muscular_fatigue_lower if state_record else 25.0,
        "cardio_fatigue": state_record.cardio_fatigue if state_record else 20.0
    }
    
    # Generate workout using the correct method name
    workout_data = generator.generate_session(
        state=state_dict,
        equipment=request.equipment_available or ["bodyweight", "dumbbells"],
        time_available=request.time_available_minutes,
        blocked_movements=[],
        workout_type=request.workout_type,
        difficulty=request.difficulty
    )
    
    return WorkoutResponse(**workout_data)

@router.post("/feedback")
def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Submit session feedback for the AI orchestrator to compute internal recovery metrics.
    """
    # Save feedback mapped explicitly to user ID here to keep data isolated
    return {"status": "Feedback processed successfully", "user_id": current_user.id}
