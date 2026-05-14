from sqlalchemy.orm import Session
from .models import MetabolicStatus, MetabolicLog
from datetime import datetime, timedelta
from app.models.progress import ProgressHistory
from app.models.nutrition import NutritionLog

class MetabolicService:
    @staticmethod
    def get_status(db: Session, user_id: int):
        status = db.query(MetabolicStatus).filter(MetabolicStatus.user_id == user_id).first()
        if not status:
            status = MetabolicStatus(user_id=user_id)
            db.add(status)
            db.commit()
            db.refresh(status)
        
        status_label = "Healthy"
        if status.adaptation_index < 0.85:
            status_label = "Slowdown"
        elif status.adaptation_index < 0.75:
            status_label = "Metabolic Adaptation Detected"
            
        return status, status_label

    @staticmethod
    def recalculate_tdee(db: Session, user_id: int):
        # 1. Fetch last 14 days of weight and intake
        days = 14
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        weights = db.query(ProgressHistory).filter(
            ProgressHistory.user_id == user_id,
            ProgressHistory.timestamp >= cutoff
        ).order_by(ProgressHistory.timestamp.asc()).all()
        
        intake = db.query(NutritionLog).filter(
            NutritionLog.user_id == user_id,
            NutritionLog.date >= cutoff.date()
        ).all()
        
        if len(weights) < 2 or len(intake) < 7:
            return None # Not enough data
            
        # Calculation Logic
        total_calories = sum(log.calories for log in intake)
        avg_intake = total_calories / len(intake)
        
        weight_diff = weights[-1].weight - weights[0].weight
        days_diff = (weights[-1].timestamp - weights[0].timestamp).days
        if days_diff == 0: days_diff = 1
        
        # TDEE = Intake - (WeightDelta * 7700 / Days)
        tdee_estimate = avg_intake - (weight_diff * 7700 / days_diff)
        
        status = db.query(MetabolicStatus).filter(MetabolicStatus.user_id == user_id).first()
        status.current_tdee = round(tdee_estimate, 0)
        
        # Adaptation Index Logic
        # Expected diff if TDEE was baseline
        expected_diff = (avg_intake - 2500) * days_diff / 7700
        if expected_diff != 0:
            status.adaptation_index = abs(weight_diff / expected_diff)
        
        db.commit()
        return status
