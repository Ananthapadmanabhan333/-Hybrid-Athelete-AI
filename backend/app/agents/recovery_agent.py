from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.api import deps
from app.models.user import User
from app.recovery_engine_v4.models import RecoveryScore

router = APIRouter()

def generate_recovery_explanation(score: float, adjustment: str) -> dict:
    # Simulates LLM generated response
    message = f"Your recovery score is {score}/100. "
    
    if adjustment == "reduce_intensity":
        message += "This indicates high fatigue. Prioritize deep sleep, hydration, and light active recovery today. Avoid heavy lifting."
    elif adjustment == "moderate_load":
        message += "You are moderately recovered. You can train today, but keep volume and intensity capped at 70%."
    else:
        message += "You are fully recovered and primed for optimal performance. Push for full intensity!"
        
    return {"insight": message, "recommended_action": adjustment}

@router.post("/analyze")
async def analyze_recovery_logs(
    target_date: date = date.today(),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    # Only 1 query to fetch the pre-computed day score
    score_record = db.query(RecoveryScore).filter(
        RecoveryScore.user_id == current_user.id,
        RecoveryScore.date == target_date
    ).first()
    
    if not score_record:
        return {"insight": "insufficient_data. Please submit your morning recovery log first."}
        
    insight = generate_recovery_explanation(score_record.recovery_score, score_record.fatigue_flag)
    return insight
