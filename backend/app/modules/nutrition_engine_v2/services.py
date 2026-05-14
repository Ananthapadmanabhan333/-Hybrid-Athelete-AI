
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import math
from . import models, schemas
from app.modules.nutrition_engine import models as nutrition_v1_models

class NutritionAggregatorService:
    @staticmethod
    def get_monthly_summary(db: Session, user_id: int, month: int, year: int) -> schemas.MonthlyCalorieSummary:
        # 1. Fetch Summary if exists
        summary = db.query(models.MonthlyCalorieSummary).filter(
            models.MonthlyCalorieSummary.user_id == user_id,
            models.MonthlyCalorieSummary.month == month,
            models.MonthlyCalorieSummary.year == year
        ).first()
        
        # 2. If not, Calculate from V1 logs (Mocking aggregation logic)
        # In real app, query DailyNutritionLogs from V1 module for this month
        
        if not summary:
            # Mock Data for Prototype
            daily_target = 2500
            days_in_month = 30
            monthly_target = daily_target * days_in_month
            consumed = 78000 # Mock consumption
            surplus = consumed - monthly_target # 3000 surplus
            projected_change = surplus / 7700.0 # ~0.38kg
            
            summary = models.MonthlyCalorieSummary(
                user_id=user_id,
                month=month,
                year=year,
                daily_calorie_target=daily_target,
                monthly_calorie_target=monthly_target,
                calories_consumed_so_far=consumed,
                surplus_or_deficit=surplus,
                projected_weight_change=round(projected_change, 2),
                goal_type=models.NutritionGoalType.BULK,
                protein_compliance_pct=85.0,
                carb_consistency_pct=90.0,
                hydration_adherence_pct=75.0,
                micronutrient_score=8.5,
                monthly_nutrition_score=82.5 # Calculated score
            )
            db.add(summary)
            db.commit()
            db.refresh(summary)
            
        return summary

    @staticmethod
    def calculate_score(summary: models.MonthlyCalorieSummary) -> float:
        # Score = (Protein * 0.35) + (Accuracy * 0.35) + (Micro * 0.2) + (Hydro * 0.1)
        # Transforming Accuracy: Closer to 0 surplus/deficit (if maintenance) or hitting target surplus
        calorie_accuracy = 90.0 # Mock
        
        score = (summary.protein_compliance_pct * 0.35) + \
                (calorie_accuracy * 0.35) + \
                (summary.micronutrient_score * 10 * 0.2) + \
                (summary.hydration_adherence_pct * 0.1)
                
        return round(score, 1)
