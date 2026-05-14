from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.nutrition import NutritionLog, WaterLog
from app.schemas.nutrition import NutritionLogCreate, NutritionLog as NutritionSchema, WaterLogCreate, WaterLog as WaterSchema

router = APIRouter()

@router.post("/meals", response_model=NutritionSchema)
def log_meal(
    *,
    db: Session = Depends(deps.get_db),
    meal_in: NutritionLogCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Log a meal.
    """
    db_obj = NutritionLog(
        **meal_in.model_dump(),
        user_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/meals", response_model=List[NutritionSchema])
def read_meals(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get meal logs.
    """
    return db.query(NutritionLog).filter(
        NutritionLog.user_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.post("/water", response_model=WaterSchema)
def log_water(
    *,
    db: Session = Depends(deps.get_db),
    water_in: WaterLogCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Log water intake.
    """
    db_obj = WaterLog(
        **water_in.model_dump(),
        user_id=current_user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/monthly-stats")
def get_monthly_nutrition_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    year: int,
    month: int,
) -> Any:
    """
    Get monthly nutrition statistics aggregated by day.
    """
    from datetime import datetime
    from calendar import monthrange
    from sqlalchemy import func
    
    # Get first and last day of month
    _, last_day = monthrange(year, month)
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, last_day, 23, 59, 59)
    
    # Get all nutrition logs for the month
    logs = db.query(NutritionLog).filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.timestamp >= start_date,
        NutritionLog.timestamp <= end_date
    ).all()
    
    # Aggregate by day
    daily_stats = {}
    for log in logs:
        day_key = log.timestamp.date().isoformat()
        if day_key not in daily_stats:
            daily_stats[day_key] = {
                "date": day_key,
                "total_calories": 0,
                "total_protein": 0,
                "total_carbs": 0,
                "total_fats": 0,
                "meal_count": 0
            }
        
        daily_stats[day_key]["total_calories"] += log.calories
        daily_stats[day_key]["total_protein"] += log.protein_g
        daily_stats[day_key]["total_carbs"] += log.carbs_g
        daily_stats[day_key]["total_fats"] += log.fats_g
        daily_stats[day_key]["meal_count"] += 1
    
    # Calculate monthly averages
    days_with_data = len(daily_stats)
    if days_with_data > 0:
        total_calories = sum(d["total_calories"] for d in daily_stats.values())
        total_protein = sum(d["total_protein"] for d in daily_stats.values())
        total_carbs = sum(d["total_carbs"] for d in daily_stats.values())
        total_fats = sum(d["total_fats"] for d in daily_stats.values())
        
        monthly_avg = {
            "avg_calories": round(total_calories / days_with_data, 1),
            "avg_protein": round(total_protein / days_with_data, 1),
            "avg_carbs": round(total_carbs / days_with_data, 1),
            "avg_fats": round(total_fats / days_with_data, 1),
            "days_tracked": days_with_data,
            "total_meals": sum(d["meal_count"] for d in daily_stats.values())
        }
    else:
        monthly_avg = {
            "avg_calories": 0,
            "avg_protein": 0,
            "avg_carbs": 0,
            "avg_fats": 0,
            "days_tracked": 0,
            "total_meals": 0
        }
    
    return {
        "month": f"{year}-{month:02d}",
        "daily_breakdown": list(daily_stats.values()),
        "monthly_averages": monthly_avg
    }

@router.get("/analysis")
def get_nutrition_analysis(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    days: int = 7,
) -> Any:
    """
    Get AI-powered nutrition analysis and recommendations.
    """
    from datetime import datetime, timedelta
    from app.ai_engine.llm_service import LLMService
    
    # Get recent nutrition data
    start_date = datetime.now() - timedelta(days=days)
    logs = db.query(NutritionLog).filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.timestamp >= start_date
    ).all()
    
    if not logs:
        return {
            "summary": "No nutrition data available for analysis. Start tracking your meals!",
            "recommendations": ["Log your meals consistently to get personalized insights"],
            "macro_balance": "insufficient_data"
        }
    
    # Calculate averages
    total_calories = sum(log.calories for log in logs)
    total_protein = sum(log.protein_g for log in logs)
    total_carbs = sum(log.carbs_g for log in logs)
    total_fats = sum(log.fats_g for log in logs)
    
    days_with_data = len(set(log.timestamp.date() for log in logs))
    
    avg_calories = round(total_calories / days_with_data, 1) if days_with_data > 0 else 0
    avg_protein = round(total_protein / days_with_data, 1) if days_with_data > 0 else 0
    avg_carbs = round(total_carbs / days_with_data, 1) if days_with_data > 0 else 0
    avg_fats = round(total_fats / days_with_data, 1) if days_with_data > 0 else 0
    
    # Calculate macro ratios
    total_macros = avg_protein * 4 + avg_carbs * 4 + avg_fats * 9
    if total_macros > 0:
        protein_pct = round((avg_protein * 4 / total_macros) * 100, 1)
        carbs_pct = round((avg_carbs * 4 / total_macros) * 100, 1)
        fats_pct = round((avg_fats * 9 / total_macros) * 100, 1)
    else:
        protein_pct = carbs_pct = fats_pct = 0
    
    # Generate AI insights
    llm = LLMService()
    context = f"""
    User: {current_user.full_name}, Weight: {current_user.current_weight_kg}kg, Activity: {current_user.activity_level}
    
    Nutrition Data (last {days} days):
    - Average Calories: {avg_calories} kcal/day
    - Average Protein: {avg_protein}g ({protein_pct}%)
    - Average Carbs: {avg_carbs}g ({carbs_pct}%)
    - Average Fats: {avg_fats}g ({fats_pct}%)
    - Tracking Consistency: {days_with_data}/{days} days
    """
    
    prompt = "Provide 2-3 specific nutrition recommendations based on this data. Be concise and actionable."
    
    try:
        ai_recommendations = llm.generate_response(context, prompt)
    except:
        ai_recommendations = "Maintain balanced macros and consistent tracking for best results."
    
    return {
        "period": f"{days} days",
        "averages": {
            "calories": avg_calories,
            "protein": avg_protein,
            "carbs": avg_carbs,
            "fats": avg_fats
        },
        "macro_ratios": {
            "protein_pct": protein_pct,
            "carbs_pct": carbs_pct,
            "fats_pct": fats_pct
        },
        "tracking_consistency": f"{days_with_data}/{days} days",
        "ai_insights": ai_recommendations,
        "recommendations": [
            f"Protein intake: {avg_protein}g/day - {'Good!' if avg_protein >= user.current_weight_kg * 1.6 else 'Consider increasing'}",
            f"Tracking consistency: {round(days_with_data/days*100)}% - {'Excellent!' if days_with_data/days > 0.8 else 'Try to log daily'}"
        ]
    }
