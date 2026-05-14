
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.api import deps
from . import models, schemas, services
from datetime import datetime, date

router = APIRouter()

@router.post("/log", response_model=schemas.RecoveryDailySummary)
def log_recovery_v3(
    *,
    db: Session = Depends(deps.get_db),
    log_in: schemas.RecoveryLogV3Create,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Log daily recovery metrics (V3) and get instant score + recommendations.
    """
    # 1. Save Log
    log = models.RecoveryLogV3(
        user_id=current_user.id,
        date=datetime.utcnow(),
        **log_in.dict()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # 2. Calculate Score
    score_result = services.RecoveryServiceV3.calculate_score(log_in)
    
    score_obj = models.RecoveryScoreV3(
        user_id=current_user.id,
        date=datetime.utcnow(),
        total_score=score_result["total_score"],
        category=score_result["category"],
        sleep_component=score_result["components"]["sleep"],
        hrv_component=score_result["components"]["hrv"],
        rhr_component=score_result["components"]["rhr"],
        soreness_component=score_result["components"]["soreness"],
        stress_component=score_result["components"]["stress"],
        hydration_component=score_result["components"]["hydration"]
    )
    db.add(score_obj)
    db.commit()
    db.refresh(score_obj)
    
    # 3. Generate Recommendations
    recs = services.RecoveryServiceV3.generate_recommendations(log_in, score_result["total_score"])
    rec_objs = []
    
    # Clear old recommendations for today? (Optional, skipping for simplicity)
    
    for r in recs:
        rec_obj = models.RecoveryRecommendation(
            user_id=current_user.id,
            date=datetime.utcnow(),
            recommendation_text=r["text"],
            type=r["type"],
            priority=r["priority"]
        )
        db.add(rec_obj)
        rec_objs.append(rec_obj)
        
    db.commit()
    
    # Return aggregated summary
    return schemas.RecoveryDailySummary(
        date=datetime.utcnow(),
        score=score_obj,
        logs=[log],
        recommendations=rec_objs
    )

@router.post("/method", response_model=schemas.RecoveryMethodLog)
def log_recovery_method(
    *,
    db: Session = Depends(deps.get_db),
    method_in: schemas.RecoveryMethodLogCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Log a specific recovery method (Sauna, Cold, etc).
    """
    method = models.RecoveryMethodLog(
        user_id=current_user.id,
        date=datetime.utcnow(),
        **method_in.dict()
    )
    db.add(method)
    db.commit()
    db.refresh(method)
    return method

@router.get("/today", response_model=schemas.RecoveryDailySummary)
def get_today_recovery(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    # Fetch latest for today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    score = db.query(models.RecoveryScoreV3).filter(
        models.RecoveryScoreV3.user_id == current_user.id,
        models.RecoveryScoreV3.date >= today_start
    ).order_by(models.RecoveryScoreV3.date.desc()).first()
    
    logs = db.query(models.RecoveryLogV3).filter(
        models.RecoveryLogV3.user_id == current_user.id,
        models.RecoveryLogV3.date >= today_start
    ).all()
    
    methods = db.query(models.RecoveryMethodLog).filter(
        models.RecoveryMethodLog.user_id == current_user.id,
        models.RecoveryMethodLog.date >= today_start
    ).all()
    
    recs = db.query(models.RecoveryRecommendation).filter(
        models.RecoveryRecommendation.user_id == current_user.id,
        models.RecoveryRecommendation.date >= today_start
    ).all()
    
    return schemas.RecoveryDailySummary(
        date=datetime.utcnow(),
        score=score,
        logs=logs,
        methods=methods,
        recommendations=recs
    )

@router.get("/weekly-summary")
def get_weekly_summary(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    return services.RecoveryServiceV3.get_weekly_summary(db, current_user.id)
