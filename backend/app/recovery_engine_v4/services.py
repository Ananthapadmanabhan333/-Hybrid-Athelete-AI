from sqlalchemy.orm import Session
from datetime import date
from app.recovery_engine_v4.models import RecoveryLog, RecoveryScore
from app.recovery_engine_v4.schemas import RecoveryLogCreate

def calculate_recovery_metrics(log: RecoveryLog, baseline_rhr: float = 60.0) -> dict:
    if not log:
        return {"status": "insufficient_data"}
        
    inv_soreness = 10 - log.soreness
    inv_stress = 10 - log.stress
    
    norm_hrv = min((log.hrv / 100) * 10, 10)
    rhr_stability = 10 if log.resting_heart_rate <= baseline_rhr else 5
    hydration_score = min(log.hydration_liters / 3.0 * 10, 10)
    
    score = (
        (log.sleep_quality * 0.25) * 10 + 
        (norm_hrv * 0.2) * 10 +
        (rhr_stability * 0.15) * 10 +
        (inv_soreness * 0.15) * 10 +
        (inv_stress * 0.15) * 10 +
        (hydration_score * 0.1) * 10
    )
    
    if score < 50:
        adj = "reduce_intensity"
    elif score <= 70:
        adj = "moderate_load"
    else:
        adj = "full_intensity"
        
    return {"score": round(score, 2), "adjustment": adj}

def save_recovery_log_and_compute(payload: RecoveryLogCreate, user_id: int, target_date: date, db: Session):
    log = RecoveryLog(user_id=user_id, date=target_date, **payload.dict())
    db.add(log)
    db.flush() 
    
    metrics = calculate_recovery_metrics(log)
    
    score_record = db.query(RecoveryScore).filter(
        RecoveryScore.user_id == user_id, 
        RecoveryScore.date == target_date
    ).first()
    
    if not score_record:
        score_record = RecoveryScore(user_id=user_id, date=target_date)
        db.add(score_record)
        
    score_record.recovery_score = metrics["score"]
    score_record.fatigue_flag = metrics["adjustment"]
    
    db.commit()
    return score_record
