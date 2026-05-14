from sqlalchemy.orm import Session
from .models import MentalState
from datetime import datetime

class MentalService:
    @staticmethod
    def log_state(db: Session, user_id: int, mood: int, motivation: int, enjoyment: int):
        # Calculate burnout risk (Mock simple logic)
        risk = (10 - mood) * 0.4 + (10 - motivation) * 0.4 + (10 - enjoyment) * 0.2
        
        state = MentalState(
            user_id=user_id,
            mood_score=mood,
            motivation_score=motivation,
            enjoyment_score=enjoyment,
            burnout_risk=risk
        )
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def get_status(db: Session, user_id: int):
        latest = db.query(MentalState).filter(
            MentalState.user_id == user_id
        ).order_by(MentalState.timestamp.desc()).first()
        
        if not latest: return None
        
        rec = "Stay consistent."
        if latest.burnout_risk > 7.0:
            rec = "High burnout risk detected. Strongly recommend a deload week."
        elif latest.motivation_score < 4:
            rec = "Motivation low. Try a group class or novelty session."
            
        return {
            "mood": latest.mood_score,
            "motivation": latest.motivation_score,
            "burnout_risk": latest.burnout_risk,
            "recommendation": rec
        }
