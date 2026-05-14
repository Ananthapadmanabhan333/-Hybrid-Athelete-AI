from sqlalchemy.orm import Session
from app.scheduling_engine.models import UserAvailability, ScheduledActivity
from app.scheduling_engine.schemas import UserAvailabilityUpdate, ActivitySubstitutionRequest
from datetime import datetime, timedelta

class SchedulingService:
    @staticmethod
    def update_availability(db: Session, user_id: int, avail_in: UserAvailabilityUpdate):
        db_avail = db.query(UserAvailability).filter(UserAvailability.user_id == user_id).first()
        if db_avail:
            db_avail.available_slots = avail_in.available_slots
            db_avail.compression_strategy = avail_in.compression_strategy
        else:
            db_avail = UserAvailability(**avail_in.dict(), user_id=user_id)
            db.add(db_avail)
        db.commit()
        db.refresh(db_avail)
        return db_avail

    @staticmethod
    def get_optimized_week(db: Session, user_id: int):
        # In a real app, this would query the adaptive_training_engine 
        # for a week's worth of workouts and fit them into availability slots
        start_of_week = datetime.utcnow()
        schedule = []
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            # Dummy logic for optimized schedule
            schedule.append({
                "date": date.isoformat(),
                "activities": [
                    {"type": "workout", "duration": 45, "status": "planned"}
                ]
            })
        return {"week_start": start_of_week, "schedule": schedule}

    @staticmethod
    def substitute_activity(db: Session, user_id: int, request: ActivitySubstitutionRequest):
        # Replaces a planned activity with a different one (e.g. Workout -> Hiking)
        original = db.query(ScheduledActivity).filter(
            ScheduledActivity.id == request.activity_id,
            ScheduledActivity.user_id == user_id
        ).first()
        
        if not original:
            return None
            
        original.status = "moved"
        
        new_activity = ScheduledActivity(
            user_id=user_id,
            activity_type=request.new_activity_type,
            scheduled_for=original.scheduled_for,
            planned_duration_minutes=request.duration_minutes,
            is_substituted=True,
            original_activity_id=original.id
        )
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        return new_activity

    @staticmethod
    def compress_workout(workout_payload: dict, available_minutes: int, strategy: str):
        """
        Logic to shrink a workout to fit a smaller time slot.
        """
        if workout_payload.get("total_estimated_duration", 60) <= available_minutes:
            return workout_payload
            
        new_payload = workout_payload.copy()
        exercises = new_payload.get("exercises", [])
        
        if strategy == "reduce_sets":
            for ex in exercises:
                if ex.get("sets", 0) > 2:
                    ex["sets"] -= 1
        elif strategy == "remove_accessory":
            # Remove exercises that aren't 'main' lifts
            new_payload["exercises"] = [ex for ex in exercises if ex.get("is_main_lift", True)]
            
        new_payload["total_estimated_duration"] = available_minutes
        new_payload["is_compressed"] = True
        return new_payload
