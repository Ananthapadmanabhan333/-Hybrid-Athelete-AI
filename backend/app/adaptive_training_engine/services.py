from typing import Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
# Imports moved inside methods to avoid circularity

class AdaptiveTrainingService:
    @staticmethod
    def get_user_profile(db: Session, user_id: int):
        from app.adaptive_training_engine.models import UserWorkoutProfile
        return db.query(UserWorkoutProfile).filter(UserWorkoutProfile.user_id == user_id).first()

    @staticmethod
    def create_or_update_profile(db: Session, user_id: int, profile_in: Any): # Using Any to avoid import at top
        from app.adaptive_training_engine.models import UserWorkoutProfile
        db_profile = db.query(UserWorkoutProfile).filter(UserWorkoutProfile.user_id == user_id).first()
        if db_profile:
            for var, value in profile_in.dict().items():
                setattr(db_profile, var, value)
        else:
            db_profile = UserWorkoutProfile(**profile_in.dict(), user_id=user_id)
            db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    def generate_workout(db: Session, user_id: int):
        from app.adaptive_training_engine.models import AdaptiveWorkoutSession
        profile = AdaptiveTrainingService.get_user_profile(db, user_id)
        if not profile:
            return None
        
        # Determine intensity adjustment from previous sessions
        adjustment = AdaptiveTrainingService._calculate_intensity_adjustment(db, user_id)
        
        # Placeholder for complex generation logic
        # In a real production app, this would call the ExerciseLibraryV2 and an LLM or Rule-Engine
        workout_payload = {
            "session_name": f"{profile.goal_type.capitalize()} Focus Session",
            "exercises": [
                {
                    "name": "Adaptive Squats",
                    "sets": 3,
                    "reps": 10,
                    "weight_kg": 60 * adjustment,
                    "tempo": "3-1-1",
                    "notes": "Focus on depth"
                },
                {
                    "name": "Pushups",
                    "sets": 3,
                    "reps": 12,
                    "rpe_target": 7
                }
            ],
            "total_estimated_duration": profile.session_duration_preference
        }
        
        new_session = AdaptiveWorkoutSession(
            user_id=user_id,
            scheduled_date=datetime.utcnow() + timedelta(days=1),
            workout_payload=workout_payload,
            intensity_adjustment=adjustment,
            status="scheduled"
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    @staticmethod
    def _calculate_intensity_adjustment(db: Session, user_id: int) -> float:
        from app.adaptive_training_engine.models import AdaptiveWorkoutSession
        # Get last completed session
        last_session = db.query(AdaptiveWorkoutSession).filter(
            AdaptiveWorkoutSession.user_id == user_id,
            AdaptiveWorkoutSession.status == "completed"
        ).order_by(AdaptiveWorkoutSession.actual_start_at.desc()).first()
        
        if not last_session:
            return 1.0 # Base intensity
        
        # Basic progression logic
        # If last was successful, increase slightly. If missed, maybe hold or decrease.
        return last_session.intensity_adjustment * 1.05 # Simple 5% overload for demo

    @staticmethod
    def update_performance(db: Session, user_id: int, update: Any):
        from app.adaptive_training_engine.models import AdaptiveWorkoutSession
        session = db.query(AdaptiveWorkoutSession).filter(
            AdaptiveWorkoutSession.id == update.session_id,
            AdaptiveWorkoutSession.user_id == user_id
        ).first()
        
        if not session:
            return None
            
        session.status = "completed" if update.completed_as_planned else "partially_completed"
        session.actual_duration_minutes = update.duration_minutes
        session.actual_start_at = datetime.utcnow()
        # In a real app, we'd store more detailed performance metrics here
        
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_next_session(db: Session, user_id: int):
        from app.adaptive_training_engine.models import AdaptiveWorkoutSession
        return db.query(AdaptiveWorkoutSession).filter(
            AdaptiveWorkoutSession.user_id == user_id,
            AdaptiveWorkoutSession.status == "scheduled"
        ).order_by(AdaptiveWorkoutSession.scheduled_date.asc()).first()
