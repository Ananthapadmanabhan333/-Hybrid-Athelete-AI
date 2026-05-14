import json
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.training import TrainingSession, TrainingType
from app.models.daily_log import DailyLog
from app.modules.performance_core.models import PerformanceSummary

def generate_coach_insight(payload: dict) -> str:
    # Simulates an LLM parsing the structured JSON payload strictly
    strength = payload.get("strength", 0)
    fatigue = payload.get("fatigue", 0)
    
    if fatigue > 80:
        insight = f"High fatigue detected ({fatigue:.1f}%). Prioritize recovery."
    elif strength > 70:
        insight = f"Strength is optimal ({strength:.1f}). Push for progressive overload."
    else:
        insight = "Performance balanced. Keep up consistency."
        
    return json.dumps({"insight": insight})

def compute_daily_performance(user_id: int, target_date: date, db: Session):
    # 1. Fetch recent metrics (7-day window)
    start_date = target_date - timedelta(days=7)
    
    sessions = db.query(TrainingSession).filter(
        TrainingSession.user_id == user_id,
        TrainingSession.started_at >= start_date,
        TrainingSession.started_at <= target_date + timedelta(days=1)
    ).all()
    
    # 2. Deterministic math
    strength_load = 0.0
    endurance_load = 0.0
    fatigue_raw = 0.0
    
    for session in sessions:
        rpe = session.rpe if session.rpe else 5
        duration = session.duration_minutes if session.duration_minutes else 0
        
        load = rpe * duration
        fatigue_raw += load
        
        if session.type in [TrainingType.STRENGTH, TrainingType.BOXING]:
            strength_load += load
        elif session.type in [TrainingType.CARDIO, TrainingType.ATHLETICS]:
            endurance_load += load
            
    # Scale normalization
    avg_fatigue = fatigue_raw / 7
    fatigue_index = min((avg_fatigue / 300) * 100, 100.0) 
    
    strength_score = min((strength_load / 1400) * 100, 100.0)
    endurance_score = min((endurance_load / 1400) * 100, 100.0)
    recovery_capacity = max(100.0 - fatigue_index, 0.0)
    
    # 3. AI Insight Execution (Deterministically scaled)
    payload = {
        "strength": strength_score,
        "fatigue": fatigue_index,
        "recovery": recovery_capacity
    }
    insight_json = generate_coach_insight(payload)
    
    # 4. Save to Performance Summary
    month_str = target_date.strftime("%Y-%m")
    
    summary = db.query(PerformanceSummary).filter(
        PerformanceSummary.user_id == user_id,
        PerformanceSummary.date == target_date
    ).first()
    
    if not summary:
        summary = PerformanceSummary(
            user_id=user_id,
            date=target_date,
            month=month_str
        )
        db.add(summary)
        
    summary.strength_score = round(strength_score, 2)
    summary.endurance_score = round(endurance_score, 2)
    summary.fatigue_index = round(fatigue_index, 2)
    summary.recovery_capacity = round(recovery_capacity, 2)
    summary.coach_insight_json = insight_json
    
    db.commit()
    return summary
