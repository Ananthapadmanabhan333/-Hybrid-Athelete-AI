
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from . import models, schemas
from app.modules.nutrition_engine_v2 import models as nut_v2_models

class BodyProgressService:
    @staticmethod
    def log_weight(db: Session, user_id: int, log_in: schemas.BodyWeightLogCreate) -> models.BodyWeightLog:
        log = models.BodyWeightLog(
            user_id=user_id,
            date=datetime.utcnow(),
            weight=log_in.weight,
            body_fat_percentage=log_in.body_fat_percentage,
            muscle_mass_estimate=log_in.muscle_mass_estimate
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_charts_data(db: Session, user_id: int) -> schemas.BodyChartsResponse:
        # 1. Fetch Weight Logs
        logs = db.query(models.BodyWeightLog).filter(
            models.BodyWeightLog.user_id == user_id
        ).order_by(models.BodyWeightLog.date.asc()).all()
        
        # 2. Get Nutrition Context for Logic
        # (Assuming current month surplus/deficit determines "gain" or "loss" mode context)
        # For prototype, we generate mock chart points based on logs
        
        gain_points = []
        loss_points = []
        
        for log in logs:
            # Map logs to chart points
            # Gain Chart: Weight vs Muscle Est
            gain_points.append(schemas.ChartDataPoint(
                date=log.date, 
                value=log.weight,
                secondary_value=log.muscle_mass_estimate or (log.weight * 0.45) # Mock muscle ~45%
            ))
            
            # Loss Chart: Weight vs Fat Est
            # Fat Mass = Weight * (BodyFat% / 100)
            fat_mass = log.weight * ((log.body_fat_percentage or 20) / 100.0)
            loss_points.append(schemas.ChartDataPoint(
                date=log.date, 
                value=log.weight,
                secondary_value=fat_mass
            ))
            
        return schemas.BodyChartsResponse(
            gain_chart=gain_points,
            loss_chart=loss_points,
            summary=None # TODO: implement summary calculation
        )
