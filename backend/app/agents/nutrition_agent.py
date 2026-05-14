from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from calendar import monthrange
from app.api import deps
from app.models.user import User
from app.models.nutrition import NutritionLog
from app.modules.nutrition_engine_v2.models import MonthlyCalorieSummary
from app.recovery_engine_v4.models import RecoveryScore
from app.modules.body_progress_engine.models import BodyWeightLog

from app.agents.nutrition_llm_agent import NutritionLLMAgent

router = APIRouter()
nutrition_agent = NutritionLLMAgent()

class NutritionQueryPayload(BaseModel):
    query: str
    
class ChatMessageLog(BaseModel):
    is_user: bool
    text: str

class NutritionChatPayload(BaseModel):
    query: str
    history: List[ChatMessageLog] = []


def _get_last_7_days_logs(current_user: User, db: Session) -> List[NutritionLog]:
    start_dt = datetime.utcnow() - timedelta(days=7)
    return (
        db.query(NutritionLog)
        .filter(
            NutritionLog.user_id == current_user.id,
            NutritionLog.timestamp >= start_dt,
        )
        .all()
    )


def _get_monthly_calorie_summary(current_user: User, db: Session) -> Optional[MonthlyCalorieSummary]:
    today = date.today()
    return (
        db.query(MonthlyCalorieSummary)
        .filter(
            MonthlyCalorieSummary.user_id == current_user.id,
            MonthlyCalorieSummary.year == today.year,
            MonthlyCalorieSummary.month == today.month,
        )
        .first()
    )


def _get_recovery_score(current_user: User, db: Session) -> Optional[float]:
    today = date.today()
    record = (
        db.query(RecoveryScore)
        .filter(
            RecoveryScore.user_id == current_user.id,
            RecoveryScore.date == today,
        )
        .first()
    )
    return record.recovery_score if record else None


def _get_weight_trend(current_user: User, db: Session) -> str:
    start_dt = datetime.utcnow() - timedelta(days=30)
    logs = (
        db.query(BodyWeightLog)
        .filter(
            BodyWeightLog.user_id == current_user.id,
            BodyWeightLog.date >= start_dt,
        )
        .order_by(BodyWeightLog.date.asc())
        .all()
    )
    if len(logs) < 2:
        return "insufficient_data"

    first = logs[0].weight
    last = logs[-1].weight
    if first is None or last is None:
        return "insufficient_data"

    if last > first + 0.5:
        return "increasing"
    if last < first - 0.5:
        return "decreasing"
    return "stable"


def analyze_nutrition_context(current_user: User, db: Session) -> dict:
    """
    Build a deterministic, structured context object for the nutrition agents.

    This function performs only simple aggregations and uses existing DB models.
    """
    logs = _get_last_7_days_logs(current_user, db)

    if not logs:
        return {"error": "insufficient_data"}

    total_protein = sum((log.protein_g or 0.0) for log in logs)
    total_calories = sum((log.calories or 0) for log in logs)

    # Weekly targets (safe deterministic defaults)
    target_protein_weekly = 150 * 7
    target_calories_weekly = 2500 * 7

    avg_daily_calories = round(total_calories / 7, 0) if total_calories else 0
    avg_daily_protein = round(total_protein / 7, 0) if total_protein else 0

    protein_compliance_pct = (
        round((total_protein / target_protein_weekly) * 100, 2)
        if target_protein_weekly > 0 and total_protein > 0
        else 0.0
    )

    monthly_summary = _get_monthly_calorie_summary(current_user, db)
    recovery_score = _get_recovery_score(current_user, db)
    weight_trend = _get_weight_trend(current_user, db)

    monthly_payload = (
        {
            "daily_calorie_target": monthly_summary.daily_calorie_target,
            "monthly_calorie_target": monthly_summary.monthly_calorie_target,
            "calories_consumed_so_far": monthly_summary.calories_consumed_so_far,
            "surplus_or_deficit": monthly_summary.surplus_or_deficit,
            "projected_weight_change": monthly_summary.projected_weight_change,
            "protein_compliance_pct": monthly_summary.protein_compliance_pct,
            "hydration_adherence_pct": monthly_summary.hydration_adherence_pct,
            "monthly_nutrition_score": monthly_summary.monthly_nutrition_score,
        }
        if monthly_summary
        else None
    )

    return {
        "goal": getattr(current_user, "fitness_goal", "hybrid_muscle_gain"),
        "last_7d": {
            "total_calories": total_calories,
            "avg_daily_calories": avg_daily_calories,
            "total_protein_g": round(total_protein, 1),
            "avg_daily_protein_g": avg_daily_protein,
            "protein_compliance_pct": protein_compliance_pct,
        },
        "monthly_calorie_summary": monthly_payload or "insufficient_data",
        "recovery_score": recovery_score if recovery_score is not None else "insufficient_data",
        "weight_trend": weight_trend,
    }

@router.post("/analyze")
async def analyze_nutrition(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    context = analyze_nutrition_context(current_user, db)
    
    if "error" in context:
        return {
            "summary_insight": "Insufficient data to generate insight. Please log your meals for at least 1 day.",
            "actionable_steps": ["Start logging your meals using the tracker."],
            "warning": "No data found."
        }
    
    insights = nutrition_agent.generate_insights(context)
    # The analyze_nutrition_compliance function returns issues directly, but now the LLM handles it format.
    return insights

@router.post("/chat")
async def chat_nutrition(
    payload: NutritionChatPayload,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    context = analyze_nutrition_context(current_user, db)
    
    if "error" in context:
         return {"response": {"message": "Please log at least one day of nutrition so I can answer your query accurately."}}
    
    chat_response = nutrition_agent.chat_response(
        context=context,
        chat_history=[h.dict() for h in payload.history],
        user_message=payload.query
    )
    
    return {"response": {"message": chat_response}}
