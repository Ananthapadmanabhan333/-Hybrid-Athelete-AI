
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, List
from app.api import deps
from . import models, schemas, services
from datetime import datetime

router = APIRouter()

@router.get("/monthly-summary", response_model=schemas.MonthlyCalorieSummary)
def get_monthly_summary(
    month: int = datetime.utcnow().month,
    year: int = datetime.utcnow().year,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    return services.NutritionAggregatorService.get_monthly_summary(db, current_user.id, month, year)

@router.get("/insights", response_model=schemas.NutritionInsights)
def get_monthly_insights(
    month: int = datetime.utcnow().month,
    year: int = datetime.utcnow().year,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    # Logic to generate insights based on summary
    summary = services.NutritionAggregatorService.get_monthly_summary(db, current_user.id, month, year)
    
    tips = []
    if summary.protein_compliance_pct < 80:
        tips.append("Increase protein intake at breakfast to hit targets.")
    if summary.hydration_adherence_pct < 80:
        tips.append("Hydration is low. Carry a water bottle.")
        
    return schemas.NutritionInsights(
        insights=[
            f"You are ${summary.surplus_or_deficit} calories away from your monthly target.",
            f"Projected weight change: {summary.projected_weight_change} kg"
        ],
        actionable_tips=tips,
        status="On Track" if summary.monthly_nutrition_score > 80 else "Needs Attention"
    )

from .extension_schemas import MacroAdjustmentOut, NutritionCoachChatRequest, NutritionCoachChatResponse
from .macro_service import MacroService
from .nutrition_coach_service import NutritionCoachService
from app.models.user import User

@router.get("/targets", response_model=MacroAdjustmentOut)
def get_nutrition_targets(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    targets = MacroService.get_todays_targets(db, current_user.id)
    if not targets:
        # Fallback calculate
        targets = MacroService.calculate_targets(db, current_user.id, "medium")
    return targets

@router.get("/recommendations", response_model=List[dict])
def get_nutrition_recommendations(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return NutritionCoachService.get_recommendations(db, current_user.id)

@router.post("/medical-coach/chat", response_model=NutritionCoachChatResponse)
def nutrition_coach_chat(
    request: NutritionCoachChatRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return NutritionCoachService.chat(db, current_user.id, request.message)
