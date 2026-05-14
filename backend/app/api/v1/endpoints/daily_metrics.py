from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.api import deps
from app.models.user import User
from app.models.daily_log import DailyLog
from app.schemas.daily_log import DailyLog as DailyLogSchema, DailyLogUpdate
from app.ai_engine.ai_analyzer import AIAnalyzer

router = APIRouter()
analyzer = AIAnalyzer()

@router.get("/today", response_model=DailyLogSchema)
def get_today_metrics(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get today's metrics for the current user.
    Creates a new daily log if one doesn't exist for today.
    """
    today = date.today()
    
    # Try to get existing log for today
    daily_log = db.query(DailyLog).filter(
        DailyLog.user_id == current_user.id,
        DailyLog.date == today
    ).first()
    
    # Create if doesn't exist
    if not daily_log:
        daily_log = DailyLog(
            user_id=current_user.id,
            date=today,
            total_calories_in=0,
            total_training_minutes=0,
            recovery_score=0,
            sleep_hours=0.0
        )
        db.add(daily_log)
        db.commit()
        db.refresh(daily_log)
    
    return daily_log

@router.put("/today", response_model=DailyLogSchema)
def update_today_metrics(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    metrics_update: DailyLogUpdate,
) -> Any:
    """
    Update today's metrics.
    Auto-creates daily log if it doesn't exist.
    """
    today = date.today()
    
    # Get or create today's log
    daily_log = db.query(DailyLog).filter(
        DailyLog.user_id == current_user.id,
        DailyLog.date == today
    ).first()
    
    if not daily_log:
        daily_log = DailyLog(
            user_id=current_user.id,
            date=today
        )
        db.add(daily_log)
    
    # Update fields
    update_data = metrics_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:  # Only update non-None values
            setattr(daily_log, field, value)
    
    db.commit()
    db.refresh(daily_log)
    
    return daily_log

@router.get("/today/insights")
def get_today_insights(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get AI-powered insights based on today's metrics and recent history.
    """
    try:
        # Get comprehensive analysis
        analysis = analyzer.analyze_user_comprehensive(current_user, db, days=7)
        
        # Get today's specific metrics
        today = date.today()
        today_log = db.query(DailyLog).filter(
            DailyLog.user_id == current_user.id,
            DailyLog.date == today
        ).first()
        
        today_metrics = {
            "calories": today_log.total_calories_in if today_log else 0,
            "training_minutes": today_log.total_training_minutes if today_log else 0,
            "sleep_hours": today_log.sleep_hours if today_log else 0,
            "recovery_score": today_log.recovery_score if today_log else 0
        }
        
        return {
            "today": today_metrics,
            "insights": analysis["insights"],
            "patterns": analysis["patterns"],
            "weekly_averages": analysis["metrics"]
        }
    except Exception as e:
        print(f"Error generating insights: {e}")
        return {
            "today": {},
            "insights": {
                "summary": "Keep up the great work!",
                "priority_recommendations": ["Stay consistent with your training"],
                "motivational_message": "Every day is a new opportunity to improve!"
            },
            "patterns": {"issues": [], "positive_patterns": []},
            "weekly_averages": {}
        }
