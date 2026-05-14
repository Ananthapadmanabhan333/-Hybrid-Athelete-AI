
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session
from app.api import deps
from . import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/log-micronutrient", response_model=schemas.MicronutrientLog)
def log_micronutrient(
    *,
    db: Session = Depends(deps.get_db),
    log_in: schemas.MicronutrientLogCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Log a micronutrient intake.
    """
    log = models.MicronutrientLog(
        user_id=current_user.id,
        date=datetime.utcnow(),
        **log_in.dict()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.post("/generate-plan", response_model=schemas.NutritionPlan)
def generate_nutrition_plan(
    *,
    db: Session = Depends(deps.get_db),
    plan_in: schemas.NutritionPlanCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Generate a nutrition plan (Mock for now, would use AI logic).
    """
    plan = models.NutritionPlan(
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        **plan_in.dict()
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

@router.get("/monthly-summary", response_model=schemas.MonthlyNutritionGoal)
def get_monthly_summary(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    # Use 1st day of current month
    current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    summary = db.query(models.MonthlyNutritionGoal).filter(
        models.MonthlyNutritionGoal.user_id == current_user.id,
        models.MonthlyNutritionGoal.month == current_month
    ).first()
    
    if not summary:
        # Create default if missing
        summary = models.MonthlyNutritionGoal(
            user_id=current_user.id,
            month=current_month,
            monthly_calorie_target=2000 * 30, # Default 2000/day
            current_monthly_calories=0,
            projected_weight_change=0.0
        )
        db.add(summary)
        db.commit()
        db.refresh(summary)
        
    return summary
